from .config import Config
import os
import sys
sys.path.append(os.path.dirname(__file__))
import gdown 
import torch
import torch.nn.functional as F
import numpy as np
import json
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse
import cv2
import warnings
from PIL import Image as PIL_Image
import numpy as np
warnings.filterwarnings("ignore")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class PytorchCaption():
    def __init__(self, beam_size=5, smooth=True):

        model_folder_path = os.path.join(os.path.expanduser("~"), ".alternat")
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        model_file_path = os.path.join(model_folder_path, Config.CAPTION_MODEL_NAME)

        wordmap_file_path = os.path.join(model_folder_path, Config.WORDMAP_FILE_NAME)

        if not os.path.isfile(model_file_path):
            print("Downloading caption model at : ", model_file_path)
            url = Config.CAPTION_MODEL_URL
            output = 'BEST_checkpoint_coco_5_cap_per_img_5_min_word_freq.pth.tar'
            gdown.download(url, model_file_path, quiet=False)

        if not os.path.isfile(wordmap_file_path):
            print("Downloading wordmap file at : ", wordmap_file_path)
            url = Config.WORDMAP_FILE_URL
            output = wordmap_file_path
            gdown.download(url, wordmap_file_path, quiet=False)
            
        # Load model
        self.checkpoint = torch.load(model_file_path, map_location=str(device))
        self.decoder = self.checkpoint['decoder']
        self.decoder = self.decoder.to(device)
        self.decoder.eval()
        self.encoder = self.checkpoint['encoder']
        self.encoder = self.encoder.to(device)
        self.encoder.eval()
        # Load word map (word2ix)
        with open(wordmap_file_path, 'r') as j:
            self.word_map = json.load(j)
        self.rev_word_map = {v: k for k, v in self.word_map.items()}  # ix2word
        self.beam_size = beam_size

    def getCaptions(self, image):
        # Encode, decode with attention and beam search
        seq, alphas, final_score = self.caption_image_beam_search(self.encoder, self.decoder, image, self.word_map, self.beam_size)
        final_score = final_score.item()
        if final_score > Config.SCORE_MAX:
            final_score = Config.SCORE_MAX
        if final_score < Config.SCORE_MIN:
            final_score = Config.SCORE_MIN
        normalized_score = (final_score - Config.SCORE_MIN)/(Config.SCORE_MAX - Config.SCORE_MIN)
        caption = self.get_caption_from_seq(seq, self.rev_word_map)
        return caption, normalized_score

    def get_caption_from_seq(self, seq, rev_word_map):
        """
        :param seq: caption
        :param rev_word_map: reverse word mapping, i.e. ix2word
        """
        words = [rev_word_map[ind] for ind in seq]
        caption = ""
        for t in range(len(words)):
            if t > 50:
                break
            if t != 0 and t != (len(words)-1):
                caption = caption + " " + words[t]
        return caption


    def caption_image_beam_search(self, encoder, decoder, img, word_map, beam_size=5):
        """
        Reads an image and captions it with beam search.

        :param encoder: encoder model
        :param decoder: decoder model
        :param image_path: path to image
        :param word_map: word map
        :param beam_size: number of sequences to consider at each decode-step
        :return: caption, weights for visualization
        """

        k = beam_size
        vocab_size = len(word_map)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if len(img.shape) == 2:
            img = img[:, :, np.newaxis]
            img = np.concatenate([img, img, img], axis=2)
        img = cv2.resize(img, (256, 256))
        img = img.transpose(2, 0, 1)
        img = img / 255.
        img = torch.FloatTensor(img).to(device)
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])
        transform = transforms.Compose([normalize])
        image = transform(img)  # (3, 256, 256)

        # Encode
        image = image.unsqueeze(0)  # (1, 3, 256, 256)
        encoder_out = encoder(image)  # (1, enc_image_size, enc_image_size, encoder_dim)
        enc_image_size = encoder_out.size(1)
        encoder_dim = encoder_out.size(3)

        # Flatten encoding
        encoder_out = encoder_out.view(1, -1, encoder_dim)  # (1, num_pixels, encoder_dim)
        num_pixels = encoder_out.size(1)

        # We'll treat the problem as having a batch size of k
        encoder_out = encoder_out.expand(k, num_pixels, encoder_dim)  # (k, num_pixels, encoder_dim)

        # Tensor to store top k previous words at each step; now they're just <start>
        k_prev_words = torch.LongTensor([[word_map['<start>']]] * k).to(device)  # (k, 1)

        # Tensor to store top k sequences; now they're just <start>
        seqs = k_prev_words  # (k, 1)

        # Tensor to store top k sequences' scores; now they're just 0
        top_k_scores = torch.zeros(k, 1).to(device)  # (k, 1)

        # Tensor to store top k sequences' alphas; now they're just 1s
        seqs_alpha = torch.ones(k, 1, enc_image_size, enc_image_size).to(device)  # (k, 1, enc_image_size, enc_image_size)

        # Lists to store completed sequences, their alphas and scores
        complete_seqs = list()
        complete_seqs_alpha = list()
        complete_seqs_scores = list()

        # Start decoding
        step = 1
        h, c = decoder.init_hidden_state(encoder_out)

        # s is a number less than or equal to k, because sequences are removed from this process once they hit <end>
        while True:

            embeddings = decoder.embedding(k_prev_words).squeeze(1)  # (s, embed_dim)

            awe, alpha = decoder.attention(encoder_out, h)  # (s, encoder_dim), (s, num_pixels)
            alpha = alpha.view(-1, enc_image_size, enc_image_size)  # (s, enc_image_size, enc_image_size)

            gate = decoder.sigmoid(decoder.f_beta(h))  # gating scalar, (s, encoder_dim)
            awe = gate * awe

            h, c = decoder.decode_step(torch.cat([embeddings, awe], dim=1), (h, c))  # (s, decoder_dim)

            scores = decoder.fc(h)  # (s, vocab_size)
            scores = F.log_softmax(scores, dim=1)


            # Add
            scores = top_k_scores.expand_as(scores) + scores  # (s, vocab_size)

            # For the first step, all k points will have the same scores (since same k previous words, h, c)
            if step == 1:
                top_k_scores, top_k_words = scores[0].topk(k, 0, True, True)  # (s)
            else:
                # Unroll and find top scores, and their unrolled indices
                top_k_scores, top_k_words = scores.view(-1).topk(k, 0, True, True)  # (s)
            
            # Convert unrolled indices to actual indices of scores
            prev_word_inds = top_k_words / vocab_size  # (s)
            next_word_inds = top_k_words % vocab_size  # (s)
            #prev_word_inds = prev_word_inds.long()
            #next_word_inds = next_word_inds.long()
            # Add new words to sequences, alphas
            seqs = torch.cat([seqs[prev_word_inds], next_word_inds.unsqueeze(1)], dim=1)  # (s, step+1)
            seqs_alpha = torch.cat([seqs_alpha[prev_word_inds], alpha[prev_word_inds].unsqueeze(1)],
                                dim=1)  # (s, step+1, enc_image_size, enc_image_size)

            # Which sequences are incomplete (didn't reach <end>)?
            incomplete_inds = [ind for ind, next_word in enumerate(next_word_inds) if
                            next_word != word_map['<end>']]
            complete_inds = list(set(range(len(next_word_inds))) - set(incomplete_inds))

            # Set aside complete sequences
            if len(complete_inds) > 0:
                complete_seqs.extend(seqs[complete_inds].tolist())
                complete_seqs_alpha.extend(seqs_alpha[complete_inds].tolist())
                complete_seqs_scores.extend(top_k_scores[complete_inds])
            k -= len(complete_inds)  # reduce beam length accordingly

            # Proceed with incomplete sequences
            if k == 0:
                break
            seqs = seqs[incomplete_inds]
            seqs_alpha = seqs_alpha[incomplete_inds]
            h = h[prev_word_inds[incomplete_inds]]
            c = c[prev_word_inds[incomplete_inds]]
            encoder_out = encoder_out[prev_word_inds[incomplete_inds]]
            top_k_scores = top_k_scores[incomplete_inds].unsqueeze(1)
            k_prev_words = next_word_inds[incomplete_inds].unsqueeze(1)

            # Break if things have been going on too long
            if step > 50:
                break
            step += 1

        #("complete_seqs_scores",complete_seqs_scores)
        i = complete_seqs_scores.index(max(complete_seqs_scores))
        seq = complete_seqs[i]
        alphas = complete_seqs_alpha[i]
        final_score = complete_seqs_scores[i]

        return seq, alphas, final_score

