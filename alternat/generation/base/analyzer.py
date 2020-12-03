from .actions import SupportedActions
from .config import AnalyzerConf
from alternat.generation.utilities import save_json_to_disk
from PIL import Image
from io import BytesIO
import base64, os
from alternat.generation.exceptions import InputImageNotAvailable


class AnalyzeImageBase:
    """Base class to implement generator driver.
    """
    def __init__(self):
        self.actions = SupportedActions()
        self.data = {key: "" for key in self.actions.get_all()}
        self.filename_postfix = "analyzer"
        self.config = AnalyzerConf

    @staticmethod
    def _base64_to_pil(base64_image):
        """Creates PIL Image object from base64 image

        :param base64_image: base64 image string.
        :type base64_image: [type]
        :return: [description]
        :rtype: [type]
        """
        im = Image.open(BytesIO(base64.b64decode(base64_image)))
        return im

    @staticmethod
    def _local_image_to_pil(abs_image_path: str):
        """Creates PIL Image object from image on disk.

        :param abs_image_path: Absolute path to image on disk.
        :type abs_image_path: str
        :return: [description]
        :rtype: [type]
        """
        im = Image.open(abs_image_path)
        return im

    @staticmethod
    def pil_to_image_content(im: Image, image_format: str = None):
        """Generate content of image from PIL Image object

        :param im: PIL Image object
        :type im: Image
        :param image_format: Image format (jpg / jpeg / png), defaults to None (JPEG)
        :type image_format: str, optional
        :return: [description]
        :rtype: [type]
        """
        buffered = BytesIO()

        if image_format is None:

            # convert to rgb format
            rgb_im = im.convert('RGB')
            img_format = "JPEG"
            rgb_im.save(buffered, format=img_format)
        else:
            img_format = image_format
            im.save(buffered, format=img_format)

        content = buffered.getvalue()
        return content

    def extract_metadata(self, base64_image: str = None, image_path: str = None):
        """Process the image to add metadata

        :param base64_image: base64 image string, defaults to None
        :type base64_image: str, optional
        :param image_path: path to image on disk, defaults to None
        :type image_path: str, optional
        :raises InputImageNotAvailable: Error when both base64_image and image_path is not there - one should be present.
        :return: [description]
        :rtype: [type]
        """
        if base64_image is not None:
            im = self._base64_to_pil(base64_image)
            self.add_metadata_base64(im, base64_image)
            return im
        elif image_path is not None:
            abs_image_path = os.path.abspath(image_path)
            im = self._local_image_to_pil(abs_image_path)
            self.add_metadata_local_file(im, abs_image_path)
            return im
        else:
            raise InputImageNotAvailable()

    def add_metadata_local_file(self, im: Image, abs_image_path: str):
        """Add metadata when the image is available locally on disk

        :param im: PIL Image object.
        :type im: Image
        :param abs_image_path: Absolute path to image on disk.
        :type abs_image_path: str
        """
        width, height = im.size
        image_type = abs_image_path.split(".")[-1]

        self.data[self.actions.get_metadata_key()] = {
            "filename": abs_image_path.split("/")[-1],
            "filepath": abs_image_path,
            "storageType": "local",
            "width": width,
            "height": height,
            "type": image_type
        }

    def add_metadata_base64(self, im: Image, base64_image: str):
        """Adds metadata when the image is base 64 image.

        :param im: PIL Image object.
        :type im: Image
        :param base64_image: base64 image string.
        :type base64_image: str
        """
        width, height = im.size
        self.data[self.actions.get_metadata_key()] = {
            "filename": "",
            "filepath": "",
            "storageType": "base64",
            "width": width,
            "height": height,
            "type": ""
        }

    def get_conf(self):
        """Get the configuration class for driver.

        :return: Config class of driver
        :rtype: [type]
        """
        return self.config

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
        return self.data

    def is_clean(self, abs_image_path: str) -> bool:
        """Check if the image is clean.

        :param abs_image_path: Absolute path to image on disk.
        :type abs_image_path: str
        :return: [description]
        :rtype: bool
        """
        return True

    def save_result(self, result: dict, output_dir_path: str):
        """Saves result to output folder in disk.

        :param result: Result JSON genearted by driver.
        :type result: dict
        :param output_dir_path: Path to directory where the results should be saved.
        :type output_dir_path: str
        :return: [description]
        :rtype: [type]
        """
        dir_path = output_dir_path
        filename = result[self.actions.get_metadata_key()]["filename"]
        name = filename.rsplit(".", 1)[0] + "_" + self.filename_postfix
        filepath = dir_path + "/" + name + ".json"
        save_json_to_disk(dir_path, result, filepath)
        return filepath



