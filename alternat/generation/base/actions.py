class SupportedActions:
    """Supported actions in generator driver. The driver implemented should support these actions.

    :return: [description]
    :rtype: [type]
    """
    OCR = "ocr"
    DESCRIBE = "caption"
    LABELS = "labels"

    _METADATA = "metadata"

    @classmethod
    def get_all(cls) -> list:
        """Get the list of all the actions in the generator driver.

        :return: [description]
        :rtype: list
        """
        return [cls.OCR, cls.DESCRIBE, cls.LABELS]

    @classmethod
    def get_metadata_key(cls):
        """Get the name of the metadata key.

        :return: [description]
        :rtype: [type]
        """
        return cls._METADATA
