from utils import create_input_files

if __name__ == '__main__':
    # Create input files (along with word map)
    create_input_files(dataset='coco',
                       karpathy_json_path='./coco/dataset_coco.json',
                       image_folder='/media/cgdata/Mayank/alternat/a-PyTorch-Tutorial-to-Image-Captioning/coco/images',
                       captions_per_image=5,
                       min_word_freq=5,
                       output_folder='/media/cgdata/Mayank/alternat/a-PyTorch-Tutorial-to-Image-Captioning/coco/processed',
                       max_len=50)
