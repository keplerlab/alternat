class AlternatException(Exception):
    """Alternat Exception base class.

    :param Exception: [description]
    :type Exception: [type]
    """

    # Error text to be displayed
    ERROR_TEXT = ""

    def __init__(self):
        self.message = self.ERROR_TEXT
        super(AlternatException, self).__init__(self.message)


class InputImageNotAvailable(AlternatException):
    """Input image not availble exception.

    :param AlternatException: [description]
    :type AlternatException: [type]
    """

    # Error text to be displayed
    ERROR_TEXT = "Input image not found: Either base64 image or local file path is required."


class OutputDirPathNotGiven(AlternatException):
    """Output directory path not specified.

    :param AlternatException: [description]
    :type AlternatException: [type]
    """

    # Error text to be displayed
    ERROR_TEXT = "Output directory not provided to save the result."


class InvalidConfigFile(AlternatException):
    """Invalid JSON for configuration.

    :param AlternatException: [description]
    :type AlternatException: [type]
    """

    # Error text to be displayed
    ERROR_TEXT = "Need a JSON file to parse configuration. " \
                 "See sample config of Generation drivers or refer documentation for more info."


class InvalidGeneratorDriver(Exception):
    """Driver is invalid or not implemented.

    :param Exception: [description]
    :type Exception: [type]
    """

    # Error text to be displayed
    ERROR_TEXT = "Driver name is invalid !"

    def __init__(self, allowed_drivers: list):
        self.allowed_drivers = allowed_drivers
        self.message = self.ERROR_TEXT + " Allowed drivers are : " + ", ".join(self.allowed_drivers) + "."
        super(InvalidGeneratorDriver, self).__init__(self.message)


class OCRClusteringException(AlternatException):
    """Cannot process image via alternat clustering algorithm.

    :param AlternatException: [description]
    :type AlternatException: [type]
    """

    # Error text to be displayed
    ERROR_TEXT = "Clustering of OCR data is not possible."

