Extending alternat
=====================


Adding new generator driver
-----------------------------

To add a new driver, use the existing driver architecture. Alternat currently supports 3 drivers

1. google

2. azure

3. opensource

**Note:**

All the drivers need to output JSON data and adhere to the schema here :
alternat/generation/data/analyzer_output.json. **Failing to do so would impact proper functioning of the driver**.

Follow the steps to add a new driver:

1. Create a new folder with name custom inside alternat/generation

    .. code-block:: bash

      cd alternat/generation
      mkdir custom

2. Create the same file structure as in the existing drivers

    .. code-block:: bash

      # move inside **custom** folder
      cd custom

      # create the following files inside **custom** folder
      # command will differ on windows shell
      touch analyzer.py
      touch config.py

3. Copy paste the contents of config file from opensource/config.py

4. Copy paste the contents of analyzer file from opensource/analyzer.py

5. Edit the following methods in custom/analyzer.py to add your own functionality.

    1. open analyzer.py in custom/analyzer.py

    2. overwrite **describe_image** method to add your custom implementation of image captioning.

        .. code-block:: bash

          # overwrite this method to extract caption

            def describe_image(self, image: PIL_Image):
            """Describe image using your custom solution.

            :param image: PIL Image object
            :type image: PIL_Image
            """

                # add the extracted caption data here instead of empty dictionary
                # the data needs to adhere to the sample JSON data at alternat/data/analyzer_output.json
                self.data[self.actions.DESCRIBE] = {}

    3. overwrite the **extract_labels** method to add your custom implementation of getting label data.

        .. code-block:: bash

          def extract_labels(self, image: PIL_Image):
          """Extract labels of image using open source solution.

          :param image: PIL Image object.
          :type image: PIL_Image
          """

              # add the extracted label data here instead of empty dictionary
              # the data needs to adhere to the sample JSON data at alternat/data/analyzer_output.json
              self.data[self.actions.LABELS] = {}

    4. overwrite the **ocr_analysis** method to add your custom implementation for ocr extraction.

        .. code-block:: bash

          def ocr_analysis(self, image: PIL_Image):
          """Does OCR Analysis using EasyOCR.

          :param image: PIL Image object.
          :type image: PIL_Image
          """

              # add the ocr extracted data here instead of empty dictionary
              # the data needs to adhere to the sample JSON data at alternat/data/analyzer_output.json
              self.data[self.actions.OCR] = {}

6. Expose the driver to the generator library so it is available across the application. Following are the steps to the same:

    1. open alternat/generation/generator.py (This is the library for alternat)

    2. Import the Analyzer & Config class of your custom driver.

        .. code-block:: bash

          from alternat.generation.custom.config import Config as CustomAnalyzerConfig
          from alternat.generation.custom.analyze import AnalyzeImage as CustomAnalyzer

    2. find the **Drivers** class and add your custom driver there.

        .. code-block:: bash

          class Drivers:
          """Driver name for alternat Library.
          """
              OPEN = "opensource"
              MICROSOFT = "azure"
              GOOGLE = "google"

              # custom driver added here
              CUSTOM = "custom"


    3. modify **_set_current_driver** method and add your custom driver in if-elif-else statements.

        .. code-block:: bash

          # TODO: This behavior will be changed later one so no method modification is required.

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

              # custom driver added
              elif self.CURRENT_DRIVER == Drivers.CUSTOM:
                  setattr(Config, Config.CURRENT_ANALYZER.__name__, CustomAnalyzer)
              else:
                  raise InvalidGeneratorDriver(self.ALLOWED_DRIVERS)


    4. modify **_get_current_driver** method and add your custom driver in if-elif-else statements.

        .. code-block:: bash

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

              # custom driver added
              elif self.CURRENT_DRIVER == Drivers.CUSTOM:
                  current_driver_cls = CustomAnalyzerConfig
              else:
                  raise InvalidGeneratorDriver(self.ALLOWED_DRIVERS)

              return current_driver_cls


7. The new custom driver will be available for use now.

