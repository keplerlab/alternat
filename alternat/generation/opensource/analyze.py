from .config import Config
from .pytorchcaption import PytorchCaption
from alternat.generation.base.analyzer import AnalyzeImageBase
import os, json, time
import requests, functools
from PIL import Image as PIL_Image
import easyocr
from alternat.generation.exceptions import InputImageNotAvailable
import numpy as np
import cv2



class AnalyzeImage(AnalyzeImageBase):
    """Opensource driver class.

    :param AnalyzeImageBase: Driver base class.
    :type AnalyzeImageBase: [type]
    """
    def __init__(self):
        super(AnalyzeImage, self).__init__()
        self.config = Config
        self.reader = easyocr.Reader(['en'])
        self.captionworker = PytorchCaption()

    def modifyBoundingBoxData(self, bounding_box: list):
        """Transform bounding box data as per the convention. EasyOCR return bounding box info in the format
        [left, top, right, top, right, bottom, left, bottom] which is transformed to format
        [{x: left, y: top}, {x: right, y: top}, {x: right, y: bottom}, {x: left, y: bototm}].

        :param bounding_box: Bounding box data form EasyOCR.
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
        """Does OCR Analysis using EasyOCR.

        :param image: PIL Image object.
        :type image: PIL_Image
        """

        result = self.reader.readtext(self.pil_to_image_content(image))

        lines_data = []
        text = ""

        for line in result:
            confidence = line[2]
            bounding_box_data = line[0]
            line_text = line[1]
            bounding_box_arr = [float(bounding_box_data[0][0]), float(bounding_box_data[0][1]), float(bounding_box_data[1][0]),
                                float(bounding_box_data[1][1]), float(bounding_box_data[2][0]), float(bounding_box_data[2][1]),
                                float(bounding_box_data[3][0]), float(bounding_box_data[3][1])]

            lines_data.append({
                "confidence": float(round(confidence, 2)),
                "text": line_text,
                "boundingBox": self.modifyBoundingBoxData(bounding_box_arr)
            })

            text += line_text + "\n"

        final_ocr_data = {
            "text": text,
            "lines": lines_data
        }

        self.data[self.actions.OCR] = final_ocr_data

    # TODO: Add open source implementation for image captioning
    def describe_image(self, image: PIL_Image):
        """Describe image using open source solution. Not implemented right now.

        :param image: PIL Image object
        :type image: PIL_Image
        """
        opencv_image = np.array(image)
        #im_np = np.asarray(self.pil_to_image_content(image))
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
        #small = cv2.resize(opencv_image, (0,0), fx=0.25, fy=0.25) 
        #cv2.imshow("window_name", small)
        #cv2.waitKey(0)
        caption, confidence = self.captionworker.getCaptions(opencv_image)
        final_caption_data = {"text": caption, "confidence": confidence}
        self.data[self.actions.DESCRIBE] = final_caption_data

    # TODO: Add open source implementation for image labelling
    def extract_labels(self, image: PIL_Image):
        """Extract labels of image using open source solution. Not implemented righ now.

        :param image: PIL Image object.
        :type image: PIL_Image
        """

        self.data[self.actions.LABELS] = {}

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




