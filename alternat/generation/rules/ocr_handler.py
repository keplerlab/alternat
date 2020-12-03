from alternat.generation.base.action_data_handler import ActionDataHandler
from alternat.generation.config import Config as GenerationConfig
from .ocr_cluster import ClusterTree


class OCRDataHandler(ActionDataHandler):
    """Rule for processing OCR data from driver.

    :param ActionDataHandler: Base class for rule.
    :type ActionDataHandler: [type]
    """
    def __init__(self, input_data, confidence_threshold: float = None,
                 ocr_filter_threshold: float = None):
        """Initialize the handler with input data and confidence threshold (if available)

        :param input_data: Data from driver.
        :type input_data: [type]
        :param confidence_threshold: Confidence threshold to filter OCR with low threshold, defaults to None (Driver config default)
        :type confidence_threshold: float, optional
        :param ocr_filter_threshold: Confidence threshold to filter OCR data based on line height ratio to image height.
        :type ocr_filter_threshold: float, optional
        """
        super(OCRDataHandler, self).__init__(input_data)

        # CONFIDENCE THRESHOLD FOR OCR
        if confidence_threshold is None:
            self.CONFIDENCE_THRESHOLD = 0.75
        else:
            self.CONFIDENCE_THRESHOLD = confidence_threshold

        print("OCR Threshold : ", self.CONFIDENCE_THRESHOLD)

        self.OCR_HEIGHT_RATIO_TO_IMAGE_THRESHOLD = ocr_filter_threshold

        # AREA OCCUPIED THRESHOLD
        self.AREA_OCCUPIED_BY_TEXT_THRESHOLD = 0.30

        # Numbers of ocr data to show
        self.NUM_OF_OCR = 3

        self.PREFIX_TEXT = "Appears to contain text: "

        self.ocr_cluster_cls = ClusterTree()

    def has_data(self) -> bool:
        """Checks whethere OCR data is avalible in the input data.

        :return: [description]
        :rtype: bool
        """

        if self.actions.OCR in self.input_data.keys():
            ocr_data = self.input_data[self.actions.OCR]

            if len(ocr_data) > 0:
                return True
            else:
                return False
        else:
            return False

    def process_ocr(self) -> dict:
        """Process the OCR data from the driver and filter it on the basis of
        line confidence threshold value and the ratio of line height to image height. 
        Based on the configuration also invokes alternat clustering implementation (default to True)

        :return: [description]
        :rtype: dict
        """

        ocr_data = self.input_data[self.actions.OCR]
        lines_data = ocr_data["lines"]
        image_metadata = self.input_data[self.actions.get_metadata_key()]
        image_height = image_metadata["height"]
        image_width = image_metadata["width"]

        filtered_lines = list(filter(lambda l: l["confidence"] >= self.CONFIDENCE_THRESHOLD, lines_data))

        filtered_text = ""

        # only for debug
        debug_line_data = []

        total_line_area = 0

        final_lines_data = []

        for line in filtered_lines:
            line_width = abs(line["boundingBox"][1]["x"] - line["boundingBox"][0]["x"])
            line_height = abs(line["boundingBox"][3]["y"] - line["boundingBox"][0]["y"])
            line_area = line_width * line_height

            # print(" line height, image height ", line_height, image_height)

            if ((line_height / image_height) > self.OCR_HEIGHT_RATIO_TO_IMAGE_THRESHOLD):
                filtered_text += line["text"] + "\n"
                total_line_area += line_area

                final_lines_data.append(line)

            #debug array data has everything
            debug_line_data.append({
                "confidence": line["confidence"],
                "line_area": line_area,
                "text": line["text"],
                "height_ratio": round(line_height / image_height, 5),
                "height":line_height
            })

        image_area = image_height * image_width

        occupied_area_by_lines = total_line_area / image_area
        # print("Occupied Area :", occupied_area_by_lines)

        # use the default final text
        final_text = filtered_text.replace("\n", " ")

        if GenerationConfig.ENABLE_OCR_CLUSTERING:
            ocr_cluster_text = self.ocr_cluster_cls.generate_data(final_lines_data)

            if len(ocr_cluster_text) > 0:
                final_text = ocr_cluster_text

        if GenerationConfig.DEBUG:
            return {
                "text": final_text,
                "is_area_above_threshold": occupied_area_by_lines > self.AREA_OCCUPIED_BY_TEXT_THRESHOLD,
                "data": debug_line_data
            }

        else:
            return {
                "text": final_text,
                "is_area_above_threshold": occupied_area_by_lines > self.AREA_OCCUPIED_BY_TEXT_THRESHOLD
            }

    def apply(self, interim_result: dict) -> dict:
        """Process intermin result from previous rules in the chain and run OCR rule.

        :param interim_result: Intermediate results from previous rules in the chain.
        :type interim_result: dict
        :return: [description]
        :rtype: dict
        """

        if self.has_data():
            processed_ocr_data = self.process_ocr()

            if processed_ocr_data["is_area_above_threshold"]:
                alt_recommendation = self.PREFIX_TEXT + processed_ocr_data["text"] + ". " + \
                                     interim_result[self.alt_recommendation_key]
                interim_result[self.alt_recommendation_key] = alt_recommendation

                if GenerationConfig.DEBUG:
                    interim_result[self.actions.OCR] = processed_ocr_data["data"]
                else:
                    interim_result[self.actions.OCR] = self.PREFIX_TEXT + processed_ocr_data["text"]
            else:
                if len(processed_ocr_data["text"]) > 0:
                    alt_recommendation = interim_result[self.alt_recommendation_key] + self.PREFIX_TEXT + \
                                         processed_ocr_data["text"] + ". "

                    if GenerationConfig.DEBUG:
                        interim_result[self.actions.OCR] = processed_ocr_data["data"]
                    else:
                        interim_result[self.actions.OCR] = self.PREFIX_TEXT + processed_ocr_data["text"]
                else:
                    alt_recommendation = interim_result[self.alt_recommendation_key]
                    interim_result[self.actions.OCR] = ""

                interim_result[self.alt_recommendation_key] = alt_recommendation


        else:
            interim_result[self.actions.OCR] = ""

        return interim_result
