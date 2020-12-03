from alternat.generation.base.config import AnalyzerConf


class Config(AnalyzerConf):
    """Configuration class for Open source driver.

    :param AnalyzerConf: Base configuration class for driver.
    :type AnalyzerConf: [type]
    """

    # driver specific threshold for caption (used by rule engine)
    CAPTION_CONFIDENCE_THRESHOLD = 0.20

    # driver specific threshold for OCR (used by rule engine)
    OCR_CONFIDENCE_THRESHOLD = 0.30

    # driver specific threshold for label data (used by rule engine)
    LABEL_CONFIDENCE_THRESHOLD = 0.75

    # line height to image height ratio for OCR
    OCR_HEIGHT_RATIO_TO_IMAGE_THRESHOLD = 0.015


