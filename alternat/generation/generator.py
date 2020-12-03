from alternat.generation.config import Config
from alternat.generation.microsoft.config import Config as MicrosoftAnalyzerConfig
from alternat.generation.google.config import Config as GoogleAnalyzerConfig
from alternat.generation.opensource.config import Config as OpenAnalyzerConfig

from alternat.generation.microsoft.analyze import AnalyzeImage as MicrosoftAnalyzer
from alternat.generation.google.analyze import AnalyzeImage as GoogleAnalyzer
from alternat.generation.opensource.analyze import AnalyzeImage as OpenAnalyzer

from alternat.generation.rules.caption_handler import CaptionDataHandler
from alternat.generation.rules.ocr_handler import OCRDataHandler
from alternat.generation.rules.label_handler import LabelDataHandler


from .exceptions import InvalidGeneratorDriver, OutputDirPathNotGiven


class Drivers:
    """Driver name for alternat Library.
    """
    OPEN = "opensource"
    MICROSOFT = "azure"
    GOOGLE = "google"


class Generator:
    """Generator class to implement alternat Library.

    :raises InvalidGeneratorDriver: Driver Invalid
    :raises InvalidGeneratorDriver: Driver Invalid
    :raises InvalidGeneratorDriver: Driver Invalid
    :raises OutputDirPathNotGiven: Output director path is not given.
    :return: [description]
    :rtype: [type]
    """

    DEFAULT_DRIVER = Drivers.OPEN

    ALLOWED_DRIVERS = [
        Drivers.OPEN,
        Drivers.MICROSOFT,
        Drivers.GOOGLE
    ]

    def __init__(self, driver_name: str = None):
        """Initializes generator with driver to use.

        :param driver_name: Name of the driver], defaults to None (opensource)
        :type driver_name: str, optional
        :raises InvalidGeneratorDriver: Driver name is invalid or not implemented.
        """
        self.conf = Config()
        self.CURRENT_DRIVER = self.DEFAULT_DRIVER

        if driver_name is not None:
            if driver_name in self.ALLOWED_DRIVERS:
                self.CURRENT_DRIVER = driver_name
            else:
                raise InvalidGeneratorDriver(self.ALLOWED_DRIVERS)

        self._set_current_driver()

    def get_current_driver(self):
        """Get the current driver.

        :return: [description]
        :rtype: [type]
        """
        return self.CURRENT_DRIVER

    def get_config(self):
        """Get the generator level config in the form of JSON.

        :return: [description]
        :rtype: [type]
        """
        var = {}
        for v in Config.__dict__:
            if not callable(getattr(Config, v)):
                if not v.startswith("_") and not v.startswith("__"):
                    var[v] = Config.__dict__[v]
        return var

    def set_config(self, conf):
        """Sets the generator level configuration parameters passed via JSON.

        :param conf: Generator configuration parameters with values.
        :type conf: [type]
        """
        for attr in conf.keys():
            if attr in self.get_config().keys():
                setattr(Config, attr, conf[attr])

    def _set_current_driver(self):
        """Sets the current driver internally within the application.

        :raises InvalidGeneratorDriver: Driver name is invalid or not implemented.
        """
        if self.CURRENT_DRIVER == Drivers.OPEN:
            setattr(Config, Config.CURRENT_ANALYZER.__name__, OpenAnalyzer)
        elif self.CURRENT_DRIVER == Drivers.MICROSOFT:
            setattr(Config, Config.CURRENT_ANALYZER.__name__, MicrosoftAnalyzer)
        elif self.CURRENT_DRIVER == Drivers.GOOGLE:
            setattr(Config, Config.CURRENT_ANALYZER.__name__, GoogleAnalyzer)
        else:
            raise InvalidGeneratorDriver(self.ALLOWED_DRIVERS)

    def _get_current_driver_conf_cls(self):
        """Retreives the driver configuration class based on the currently driver

        :raises InvalidGeneratorDriver: Driver name is invalid or not implemented.
        :return: [description]
        :rtype: [type]
        """
        current_driver_cls = None
        if self.CURRENT_DRIVER == Drivers.OPEN:
            current_driver_cls = OpenAnalyzerConfig
        elif self.CURRENT_DRIVER == Drivers.MICROSOFT:
            current_driver_cls = MicrosoftAnalyzerConfig
        elif self.CURRENT_DRIVER == Drivers.GOOGLE:
            current_driver_cls = GoogleAnalyzerConfig
        else:
            raise InvalidGeneratorDriver(self.ALLOWED_DRIVERS)

        return current_driver_cls

    def get_driver_config(self):
        """Get the driver config in the form of JSON. Retreives public members [name: value] pair
        from the driver config class.

        :return: [description]
        :rtype: [type]
        """
        current_driver_conf_cls = self._get_current_driver_conf_cls()

        var = {}
        for v in current_driver_conf_cls.__dict__:
            if not callable(getattr(current_driver_conf_cls, v)):
                if not v.startswith("_") and not v.startswith("__"):
                    var[v] = current_driver_conf_cls.__dict__[v]
        return var

    def set_driver_config(self, conf: dict):
        """Sets the driver config parameters using the JSON passed. There is one-to-one 
        mapping between key in json and driver class public members.

        :param conf: Configuration JSON to set the driver configuration.
        :type conf: dict
        """
        current_driver_conf_cls = self._get_current_driver_conf_cls()

        for attr in conf.keys():
            if attr in self.get_driver_config().keys():
                setattr(current_driver_conf_cls, attr, conf[attr])

    def _process_image(self, image_path: str = None, output_dir_path: str = None, base64_image: str = None,
                       save: bool = True):
        """Process the image based on current driver and its configuration.

        :param image_path: Path to image on disk, defaults to None
        :type image_path: str, optional
        :param output_dir_path: Path to output directory where the results are stored, defaults to None
        :type output_dir_path: str, optional
        :param base64_image: Base64 image string, defaults to None
        :type base64_image: str, optional
        :param save: Whether to save the results in a file at specified location, defaults to True
        :type save: bool, optional
        :raises OutputDirPathNotGiven: Output directory path not given.
        :return: [description]
        :rtype: [type]
        """
        analyzer = Config.get_analyzer()

        data = analyzer.handle(image_path, base64_image)

        # TODO: Intermediate results should be saved separately
        # analyzer.save_result(data, output_dir_path)

        analyzer_conf = analyzer.get_conf()
        ocr_filter_threshold = analyzer_conf.get_ocr_height_width_to_image_ratio()
        caption_handler = CaptionDataHandler(data, analyzer_conf.get_caption_threshold())
        ocr_handler = OCRDataHandler(
            data, analyzer_conf.get_ocr_threshold(), ocr_filter_threshold
        )
        label_handler = LabelDataHandler(data, analyzer_conf.get_label_threshold())

        # Chain of responsibility
        caption_handler.set_next(ocr_handler).set_next(label_handler)
        output = caption_handler.handle()

        # the first handler in the chain also adds metadata information and saves the file to disk
        final_json = caption_handler.add_metadata(output)

        if save:
            if output_dir_path is not None:
                rules_json_filepath = caption_handler.save_result(final_json, output_dir_path)
            else:
                raise OutputDirPathNotGiven()

        return final_json

    def generate_alt_text_from_base64(self, base64_image: str):
        """Generates alt-text from base64 image string.

        :param base64_image: base64 image string
        :type base64_image: str
        :return: [description]
        :rtype: [type]
        """
        result_json = self._process_image(None, None, base64_image, False)
        return result_json

    def generate_alt_text_from_file(self, input_image_path: str, output_dir_path: str):
        """Generates alt-text from file on disk.

        :param input_image_path: Path to image to be processed.
        :type input_image_path: str
        :param output_dir_path: Path to directory where the results needs to be saved.
        :type output_dir_path: str
        :return: [description]
        :rtype: [type]
        """
        result_json = self._process_image(input_image_path, output_dir_path)
        return result_json



