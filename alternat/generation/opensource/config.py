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

    CAPTION_MODEL_URL = "https://drive.google.com/uc?id=12r6T14knvlEZuNeXFEwLgfYub1UG1ujl"

    CAPTION_MODEL_NAME = "pytorch_ver_1_4_model.pth.tar"

    WORDMAP_FILE_URL = "https://drive.google.com/uc?id=1MVrblmhJ2svQ61A6J6OZkWEI-8oySTeS"

    WORDMAP_FILE_NAME = "WORDMAP_coco_5_cap_per_img_5_min_word_freq.json"

    # If you are training a new model  empirically calculate lower and upper bounds of 
    # Scoring 
    SCORE_MIN = -10.5
    SCORE_MAX = -4.0
