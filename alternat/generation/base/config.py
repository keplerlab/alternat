class AnalyzerConf:
    """Base configuration class (driver specific) used by the rule engine.

    :return: [description]
    :rtype: [type]
    """
    # driver specific threshold for caption (used by rule engine)
    CAPTION_CONFIDENCE_THRESHOLD = 0.20

    # driver specific threshold for OCR (used by rule engine)
    OCR_CONFIDENCE_THRESHOLD = 0.75

    # driver specific threshold for label data (used by rule engine)
    LABEL_CONFIDENCE_THRESHOLD = 0.50

    # OCR height width ratio to image height width should be greater
    # than this value to pass through rule engine
    OCR_HEIGHT_RATIO_TO_IMAGE_THRESHOLD = 0.20

    @classmethod
    def get_ocr_height_width_to_image_ratio(cls):
        """Get the ratio for line height / image height used to filter out irrelevant OCR text.

        :return: [description]
        :rtype: [type]
        """
        return cls.OCR_HEIGHT_RATIO_TO_IMAGE_THRESHOLD

    @classmethod
    def get_ocr_threshold(cls):
        """Get the confidence threshold to filter OCR data.

        :return: [description]
        :rtype: [type]
        """
        return cls.OCR_CONFIDENCE_THRESHOLD

    @classmethod
    def get_label_threshold(cls):
        """Get the confidence threshold to filter label data.

        :return: [description]
        :rtype: [type]
        """
        return cls.LABEL_CONFIDENCE_THRESHOLD

    @classmethod
    def get_caption_threshold(cls):
        """Get the confidence threshold to filter caption data.

        :return: [description]
        :rtype: [type]
        """
        return cls.CAPTION_CONFIDENCE_THRESHOLD
