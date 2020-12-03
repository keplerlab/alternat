from alternat.generation.base.analyzer import AnalyzeImageBase
from google.cloud import vision
import io, os
from .config import Config
from PIL import Image as PIL_IMAGE
from alternat.generation.exceptions import InputImageNotAvailable


class AnalyzeImage(AnalyzeImageBase):
    """Google Analyzer driver class.

    :param AnalyzeImageBase: Driver base class.
    :type AnalyzeImageBase: [type]
    """
    def __init__(self):
        super(AnalyzeImage, self).__init__()
        self.config = Config

        self.params = self.config.params()

        self.set_environment_variables()

    def set_environment_variables(self):
        """Sets environment variable GOOGLE_APPLICATION_CREDENTIALS based on config.
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.params["credentials"]

    def describe_image(self, image: PIL_IMAGE):
        """Describe image (used for captioning) - Not availble in Google Computer Vision API

        :param image: [description]
        :type image: PIL_IMAGE
        """
        self.data[self.actions.DESCRIBE] = {"text": '', "confidence": 1}

    def ocr_analysis(self, image: PIL_IMAGE):
        """Does OCR analysis using Google Computer Vision API. Also runs the alternat clustering rule
        if app is configured for it.

        :param image: PIL Image object.
        :type image: PIL_IMAGE
        """

        client = vision.ImageAnnotatorClient()

        # with io.open(abs_image_path, 'rb') as image_file:
        #     content = image_file.read()

        image = vision.types.Image(content=self.pil_to_image_content(image))

        # response = client.annotate_image({
        #     "image": image,
        #     "features": [{"type": vision.enums.Feature.Type.TEXT_DETECTION}]
        # })

        response = client.document_text_detection(image=image)

        full_ocr_data = response.full_text_annotation

        final_ocr_data = {
            "text": full_ocr_data.text,
            "lines": []
        }

        lines_data = []

        pages = full_ocr_data.pages

        for page in pages:
            blocks = page.blocks

            # google doesnt not gives line level information so the blocks here become the lines
            for block in blocks:
                paragraphs = block.paragraphs
                block_text = ""
                for paragraph in paragraphs:
                    for word in paragraph.words:
                        symbols = word.symbols
                        for character in symbols:
                            block_text += character.text

                        # add a space between words
                        block_text += " "

                # a block of word has finished
                block_text += "."

                lines_data.append({
                    "confidence": round(block.confidence, 2),
                    "text": block_text,
                    "boundingBox": [{"x": coord.x, "y": coord.y} for coord in block.bounding_box.vertices]
                })

        final_ocr_data["lines"] = lines_data

        # self.data[self.actions.OCR] = lines_data
        self.data[self.actions.OCR] = final_ocr_data

    def extract_labels(self, image: PIL_IMAGE):
        """Extract labels of image using Google Computer Vision API.

        :param image: PIL Image object.
        :type image: PIL_IMAGE
        :raises Exception: Google Cloud specific error messages based on request.
        """

        client = vision.ImageAnnotatorClient()

        # with io.open(abs_image_path, 'rb') as image_file:
        #     content = image_file.read()

        image = vision.types.Image(content=self.pil_to_image_content(image))

        response = client.label_detection(image=image)
        labels = response.label_annotations
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        label_data = []
        for label in labels:
            label_data.append({
                "description": label.description,
                "confidence": label.score
            })

        self.data[self.actions.LABELS] = label_data

    def handle(self, image_path: str = None, base64_image: str = None, actions: list = None) -> dict:
        """Entry point for the driver. Implements all the action and generates data for rule engine.

        :param image_path: Path to image on disk, defaults to None
        :type image_path: str, optional
        :param base64_image: Base64 image string, defaults to None
        :type base64_image: str, optional
        :param actions: list of actions to run, defaults to None (all actions execute)
        :type actions: list, optional
        :return: [description]
        :rtype: dict
        """
        try:
            im = self.extract_metadata(base64_image, image_path)
        except InputImageNotAvailable as e:
            print("ERROR: %s" % e)
            return self.data

        if actions is None:
            actions = self.actions.get_all()

        for action in actions:
            # if feature is supported
            if action in self.actions.get_all():

                if action == self.actions.OCR:
                    self.ocr_analysis(im)
                if action == self.actions.LABELS:
                    self.extract_labels(im)
                if action == self.actions.DESCRIBE:
                    self.describe_image(im)

        return self.data
