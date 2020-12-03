from alternat.generation.base.config import AnalyzerConf


class Config(AnalyzerConf):
    """Configuration class for Azure driver.

    :param AnalyzerConf: Base configuration class for driver.
    :type AnalyzerConf: [type]
    :return: [description]
    :rtype: [type]
    """
    SUBSCRIPTION_KEY = "" # ENTER AZURE COGNITIVE SERVICE SUBSCRIPTION KEY HERE
    ENDPOINT = "https://<ENTER_PROJECT_NAME>.cognitiveservices.azure.com/" # ENTER ENDPOINT FOR COGNITIVE SERVICE API

    # set this to true if rate limit needs to be enabled
    AZURE_RATE_LIMIT_ON = True

    # The sleep time after which the next set of requests are send
    AZURE_RATE_LIMIT_TIME_IN_SEC = 30

    # the API wont process if height or width width of the image go outside of
    # these constraints
    _MIN_IMAGE_SIZE_IN_PIXEL = 50
    _MAX_IMAGE_SIZE_IN_PIXEL = 5000

    # driver specific threshold for caption (used by rule engine)
    CAPTION_CONFIDENCE_THRESHOLD = 0.20

    # driver specific threshold for OCR (used by rule engine)
    OCR_CONFIDENCE_THRESHOLD = 0.75

    # driver specific threshold for label data (used by rule engine)
    LABEL_CONFIDENCE_THRESHOLD = 0.75

    # line height to image height ratio for OCR
    OCR_HEIGHT_RATIO_TO_IMAGE_THRESHOLD = 0.015

    @classmethod
    def params(cls) -> dict:
        """Retreives the subscription key and the endpoint URL in the JSON.

        :return: [description]
        :rtype: dict
        """
        return {
            "subscription": cls.SUBSCRIPTION_KEY,
            "endpoint": cls.ENDPOINT,
        }

    def update_conf(self, conf: dict):
        """Update configuration based on parameters passed in the JSON. The class members 
        and the key in the conf JSON should match.

        :param conf: JSON object with configuration.
        :type conf: dict
        """
        self.AZURE_RATE_LIMIT_ON = conf["AZURE_RATE_LIMIT_ON"]
