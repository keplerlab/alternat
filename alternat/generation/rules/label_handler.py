from alternat.generation.base.action_data_handler import ActionDataHandler
from alternat.generation.config import Config as GenerationConfig


class LabelDataHandler(ActionDataHandler):
    """Rule for processing label data from driver.

    :param ActionDataHandler: Base class for rule.
    :type ActionDataHandler: [type]
    """
    def __init__(self, input_data, confidence_threshold: float = None):
        """Initialize the handler with input data and confidence threshold (if available)

        :param input_data: Data from driver.
        :type input_data: [type]
        :param confidence_threshold: Confidence threshold to filter labels with low threshold, defaults to None (Driver config default)
        :type confidence_threshold: float, optional
        """
        super(LabelDataHandler, self).__init__(input_data)

        # CONFIDENCE THRESHOLD FOR LABELS
        if confidence_threshold is None:
            self.CONFIDENCE_THRESHOLD = 0.50
        else:
            self.CONFIDENCE_THRESHOLD = confidence_threshold

        print("Label Threshold : ", self.CONFIDENCE_THRESHOLD)

        # Numbers of labels to show
        self.NUM_OF_LABELS = 3

    def has_data(self) -> bool:
        """Checks whethere label data is avalible in the input data.

        :return: [description]
        :rtype: bool
        """

        if self.actions.LABELS in self.input_data.keys():
            labels = self.input_data[self.actions.LABELS]

            if len(labels) > 0:
                return True
            else:
                return False
        else:
            return False

    def apply(self, interim_result: dict) -> dict:
        """Process intermin result from previous rules in the chain and run label rule.

        :param interim_result: Intermediate results from previous rules in the chain.
        :type interim_result: dict
        :return: [description]
        :rtype: dict
        """

        ocr_data_present = len(interim_result[self.actions.OCR]) > 0
        caption_data_present = len(interim_result[self.actions.DESCRIBE]) > 0

        if self.has_data():

            labels_data = self.input_data[self.actions.LABELS]
            filtered_labels = list(filter(lambda label: label["confidence"] >= self.CONFIDENCE_THRESHOLD,
                                          labels_data))

            if GenerationConfig.DEBUG:
                labels = list(map(lambda label: {"description": label["description"], "confidence": label["confidence"]},
                                  filtered_labels[:self.NUM_OF_LABELS]))
            else:
                labels = ", ".join(list(map(lambda label: label["description"], filtered_labels[:self.NUM_OF_LABELS])))
            interim_result[self.actions.LABELS] = labels

            if not ocr_data_present and not caption_data_present:

                if GenerationConfig.DEBUG:
                    interim_result[self.alt_recommendation_key] = interim_result[
                                                                      self.alt_recommendation_key] + ",".join([label["description"] for label in labels]) + "."
                else:
                    interim_result[self.alt_recommendation_key] = interim_result[self.alt_recommendation_key] + labels + "."

        else:
            interim_result[self.actions.LABELS] = ""

        return interim_result
