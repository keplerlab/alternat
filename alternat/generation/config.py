from alternat.generation.microsoft.analyze import AnalyzeImage as ImageAnalyzerMicrosoft
from alternat.generation.google.analyze import AnalyzeImage as ImageAnalyzerGoogle
from alternat.generation.opensource.analyze import AnalyzeImage as ImageAnalyzerOpen


from alternat.generation.base.analyzer import AnalyzeImageBase


class Config:
    """Configuration class for generation.

    :return: [description]
    :rtype: [type]
    """

    # Change this to "ImageAnalyzerGoogle" if you want to use Google Analyzer
    # Change this to "ImageAnalyzerMicrosoft" if you want to use Azure Analyzer
    CURRENT_ANALYZER = ImageAnalyzerOpen

    # when True, the output will also save confidence value for OCR with line height data
    # This is useful for optimizing OCR thresholds.
    DEBUG = False

    # this enables ocr clustering
    ENABLE_OCR_CLUSTERING = True

    @classmethod
    def get_analyzer(cls) -> AnalyzeImageBase:
        """Get the current analyzer.

        :return: [description]
        :rtype: AnalyzeImageBase
        """
        analyzer = getattr(cls, cls.CURRENT_ANALYZER.__name__)
        return analyzer()
