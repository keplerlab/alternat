from alternat.generation.base.action_data_handler import ActionDataHandler
from alternat.generation.config import Config as GenerationConfig


class CaptionDataHandler(ActionDataHandler):
    """Rule for processing caption data from driver.

    :param ActionDataHandler: Base class for rule.
    :type ActionDataHandler: [type]
    """
    def __init__(self, input_data: dict, confidence_threshold: float = None):
        """Initialize the handler with input data and confidence threshold (if available)

        :param input_data: Data from driver.
        :type input_data: dict
        :param confidence_threshold: Confidence threshold to filter captions with low threshold, defaults to None (Driver config default)
        :type confidence_threshold: float, optional
        """
        super(CaptionDataHandler, self).__init__(input_data)

        # CONFIDENCE THRESHOLD FILTER
        if confidence_threshold is None:
            self.CONFIDENCE_THRESHOLD = 0.20
        else:
            self.CONFIDENCE_THRESHOLD = confidence_threshold

        print("Caption Threshold : ", self.CONFIDENCE_THRESHOLD)

        self.PREFIX_TEXT = "Appears to be: "

    def has_data(self) -> bool:
        """Checks whethere caption data is avalible in the input data.

        :return: [description]
        :rtype: bool
        """

        if self.actions.DESCRIBE in self.input_data.keys():

            caption = self.input_data[self.actions.DESCRIBE]

            if len(caption) > 0:
                return True
            else:
                return False
        else:
            return False

    def apply(self, interim_result: dict) -> dict:
        """Process intermin result from previous rules in the chain and run caption rule.

        :param interim_result: Intermediate results from previous rules in the chain.
        :type interim_result: dict
        :return: [description]
        :rtype: dict
        """

        if self.has_data():
            caption_data = self.input_data[self.actions.DESCRIBE]

            if caption_data["confidence"] >= self.CONFIDENCE_THRESHOLD and len(caption_data["text"].strip()) > 0:

                caption = self.PREFIX_TEXT + caption_data["text"].strip() + ". "

                if GenerationConfig.DEBUG:
                    interim_result[self.actions.DESCRIBE] = {"caption": caption, "confidence": caption_data["confidence"]}
                else:
                    interim_result[self.actions.DESCRIBE] = caption

                interim_result[self.alt_recommendation_key] = caption
            else:
                interim_result[self.actions.DESCRIBE] = ""
                interim_result[self.alt_recommendation_key] = ""

        else:
            interim_result[self.actions.DESCRIBE] = ""
            interim_result[self.alt_recommendation_key] = ""

        return interim_result

