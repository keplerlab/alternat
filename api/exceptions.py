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


class UnsupportedImageType(AlternatException):
    """Image type is not supported

    :param AlternatException: [description]
    :type AlternatException: [type]
    """

    # Error text to be displayed
    ERROR_TEXT = "Invalid image format. Supported images formats are jpg, jpeg and png."


class InvalidImageURL(AlternatException):
    """Not a valid Image URL

    :param AlternatException: [description]
    :type AlternatException: [type]
    """

    # Error text to be displayed
    ERROR_TEXT = "Invalid Image URL."


class ImageNotLoaded(AlternatException):
    """Image URL could be loaded.

        :param AlternatException: [description]
        :type AlternatException: [type]
        """

    # Error text to be displayed
    ERROR_TEXT = "Could not load image for URL. Supported images formats are jpg, jpeg and png."
