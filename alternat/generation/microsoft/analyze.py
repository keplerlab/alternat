from .config import Config
from alternat.generation.base.analyzer import AnalyzeImageBase
import os, json, time
import time
import requests, functools
from PIL import Image as PIL_Image
import json
from alternat.generation.exceptions import InputImageNotAvailable


class AnalyzeImage(AnalyzeImageBase):
    """Azure / Microsoft Analyzer driver class.

    :param AnalyzeImageBase: Driver base class.
    :type AnalyzeImageBase: [type]
    """
    def __init__(self):
        super(AnalyzeImage, self).__init__()
        self.config = Config

        self.params = self.config.params()

        self.describe_endpoint = self.params["endpoint"] + "vision/v3.1/analyze"
        self.ocr_endpoint = self.params["endpoint"] + "vision/v3.1/read/analyze"

    def modifyBoundingBoxData(self, bounding_box: list):
        """Transform bounding box data as per the convention. Azure API return bounding box info in the format
        [left, top, right, top, right, bottom, left, bottom] which is transformed to format
        [{x: left, y: top}, {x: right, y: top}, {x: right, y: bottom}, {x: left, y: bototm}].

        :param bounding_box: Bounding box data form Azure API.
        :type bounding_box: list
        :return: [description]
        :rtype: [type]
        """

        arr = bounding_box
        return [
            {"x": arr[0], "y": arr[1]},
            {"x": arr[2], "y": arr[3]},
            {"x": arr[4], "y": arr[5]},
            {"x": arr[6], "y": arr[7]}
        ]

    def ocr_analysis(self, image: PIL_Image):
        """Does OCR Analysis using Azure Vision API.

        :param image: PIL Image object.
        :type image: PIL_Image
        """

        headers = {'Ocp-Apim-Subscription-Key': self.params["subscription"],
                   'Content-Type': 'application/octet-stream'}
        params = {'language': 'en', 'detectOrientation': 'true'}

        try:
            response = requests.post(
                self.ocr_endpoint, headers=headers, params=params, data=self.pil_to_image_content(image))
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            exception = json.loads(response.content)

            if exception["error"]["code"] == "429":

                if Config.AZURE_RATE_LIMIT_ON:
                    print("\n\nRate limited by Azure. The next call will execute after %d sec \n\n" %
                          Config.AZURE_RATE_LIMIT_TIME_IN_SEC)

                    time.sleep(Config.AZURE_RATE_LIMIT_TIME_IN_SEC)
                    self.ocr_analysis(image)
                    return

                else:
                    print("\n\nRate limited by Azure. You can enable rate limiting by "
                          "setting AZURE_RATE_LIMIT_ON in config.py\n\n")
                    return

            else:
                print("Error in sending request: ", response.content)
                return

        # Holds the URI used to retrieve the recognized text.
        operation_url = response.headers["Operation-Location"]

        # The recognized text isn't immediately available, so poll to wait for completion.
        analysis = {}
        poll = True
        while poll:
            response_final = requests.get(
                response.headers["Operation-Location"], headers=headers)
            analysis = response_final.json()

            # print(json.dumps(analysis, indent=4))

            time.sleep(1)
            if "analyzeResult" in analysis:
                poll = False
            if "status" in analysis and analysis['status'] == 'failed':
                poll = False

        lines_data = []
        text = ""

        if "analyzeResult" in analysis:
            # Extract the recognized text, with bounding boxes.
            for line in analysis["analyzeResult"]["readResults"][0]["lines"]:

                words = line["words"]
                total_words_confidence = functools.reduce(lambda a, b: a + b,
                                                          [word["confidence"] for word in words])
                average_confidence = round(total_words_confidence / len(words), 2)
                lines_data.append({
                    "text": line["text"],
                    "confidence": average_confidence,
                    "boundingBox": self.modifyBoundingBoxData(line["boundingBox"])
                })

                text += line["text"] + "\n"

        final_ocr_data = {
            "text": text,
            "lines": lines_data
        }

        self.data[self.actions.OCR] = final_ocr_data

    def describe_image(self, image: PIL_Image):
        """Describe image using Azure Vision API.

        :param image: PIL Image object
        :type image: PIL_Image
        """

        headers = {'Ocp-Apim-Subscription-Key': self.params["subscription"],
                   'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Categories,Description'}

        try:
            response = requests.post(
                self.describe_endpoint, headers=headers, params=params, data=self.pil_to_image_content(image))

            response.raise_for_status()
        except requests.exceptions.HTTPError:
            exception = json.loads(response.content)

            if exception["error"]["code"] == "429":

                if Config.AZURE_RATE_LIMIT_ON:
                    print("\n\nRate limited by Azure. The next call will execute after %d sec \n\n" %
                          Config.AZURE_RATE_LIMIT_TIME_IN_SEC)

                    time.sleep(Config.AZURE_RATE_LIMIT_TIME_IN_SEC)
                    self.describe_image(image)
                    return

                else:
                    print("\n\nRate limited by Azure. You can enable rate limiting by "
                          "setting AZURE_RATE_LIMIT_ON in config.py\n\n")
                    return

            else:
                print("Error in sending request: ", response.content)
                return

        analysis = response.json()
        # print(" DESCRIBE : ", analysis)
        caption = analysis["description"]["captions"][0]["text"]
        confidence = analysis["description"]["captions"][0]["confidence"]

        self.data[self.actions.DESCRIBE] = {"text": caption, "confidence": confidence}

    def extract_labels(self, image: PIL_Image):
        """Extract labels of image using Azure Vision API.

        :param image: PIL Image object.
        :type image: PIL_Image
        """
        headers = {'Ocp-Apim-Subscription-Key': self.params["subscription"],
                   'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Tags'}

        try:
            response = requests.post(
                self.describe_endpoint, headers=headers, params=params, data=self.pil_to_image_content(image))

            response.raise_for_status()
        except requests.exceptions.HTTPError:
            exception = json.loads(response.content)

            if exception["error"]["code"] == "429":

                if Config.AZURE_RATE_LIMIT_ON:
                    print("\n\nRate limited by Azure. The next call will execute after %d sec \n\n" %
                          Config.AZURE_RATE_LIMIT_TIME_IN_SEC)

                    time.sleep(Config.AZURE_RATE_LIMIT_TIME_IN_SEC)
                    self.extract_labels(image)
                    return

                else:
                    print("\n\nRate limited by Azure. You can enable rate limiting by "
                          "setting AZURE_RATE_LIMIT_ON in config.py\n\n")
                    return

            else:
                print("Error in sending request: ", response.content)
                return

        analysis = response.json()
        labels = analysis["tags"]

        labels_data = []

        for label in labels:
            labels_data.append({
                "description": label["name"],
                "confidence": label["confidence"]
            })

        self.data[self.actions.LABELS] = labels_data

    def resize_image(self, image: PIL_Image):
        """Resize image (maintaining aspect ratio) if width / height > 5000 pixels (API constrain from Azure)

        :param image: [description]
        :type image: PIL_Image
        """
        size = Config._MAX_IMAGE_SIZE_IN_PIXEL, Config._MAX_IMAGE_SIZE_IN_PIXEL
        image.thumbnail(size, PIL_Image.ANTIALIAS)
        # im.save(abs_image_path)

    def is_clean(self, image: PIL_Image) -> bool:
        """Check if the image has proper resolution, and is clean.

        :param image:PIL Image object.
        :type image: PIL_Image
        :return: [description]
        :rtype: bool
        """
        width, height = image.size

        if width < Config._MIN_IMAGE_SIZE_IN_PIXEL or height < Config._MIN_IMAGE_SIZE_IN_PIXEL:
            return False

        if width > Config._MAX_IMAGE_SIZE_IN_PIXEL or height > Config._MAX_IMAGE_SIZE_IN_PIXEL:
            self.resize_image(image)

        return True

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

        if self.is_clean(im):
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
        else:
            print("Image dimensions outside of bound Min: %d X %d | Max : %d X %d"
                  % (Config._MIN_IMAGE_SIZE_IN_PIXEL, Config._MIN_IMAGE_SIZE_IN_PIXEL,
                     Config._MAX_IMAGE_SIZE_IN_PIXEL, Config._MAX_IMAGE_SIZE_IN_PIXEL))
            print("Skipping this image")

        return self.data




