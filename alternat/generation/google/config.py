import os
import json
import pathlib
from alternat.generation.base.config import AnalyzerConf


class Config(AnalyzerConf):
    """Configuration class for Google driver.

    :param AnalyzerConf: Base configuration class for driver.
    :type AnalyzerConf: [type]
    :return: [description]
    :rtype: [type]
    """

    # The filename of the credentials file
    _GOOGLE_APPLICATION_CREDENTIALS_FILENAME = 'key.json'

    # The relative path to directory in which the credentials file should exist
    _RELATIVE_CREDENTIALS_DIR_PATH = "credentials"

     # driver specific threshold for caption (used by rule engine)
    CAPTION_CONFIDENCE_THRESHOLD = 0.00

    # driver specific threshold for OCR (used by rule engine)
    OCR_CONFIDENCE_THRESHOLD = 0.70

    # driver specific threshold for label data (used by rule engine)
    LABEL_CONFIDENCE_THRESHOLD = 0.50

    # line height to image height ratio for OCR
    OCR_HEIGHT_RATIO_TO_IMAGE_THRESHOLD = 0.015

    # absolute path to credential file
    ABSOLUTE_PATH_TO_CREDENTIAL_FILE = ""

    @classmethod
    def params(cls) -> dict:
        """Get the google credential file path.

        :return: [description]
        :rtype: [type]
        """

        if len(cls.ABSOLUTE_PATH_TO_CREDENTIAL_FILE) > 0:
            credentials = cls.ABSOLUTE_PATH_TO_CREDENTIAL_FILE
        else:

            abs_path_file = pathlib.Path(__file__).parent.absolute()

            credentials = os.path.join(abs_path_file, cls._RELATIVE_CREDENTIALS_DIR_PATH,
                                       cls._GOOGLE_APPLICATION_CREDENTIALS_FILENAME)
        return {
            "credentials": credentials
        }



