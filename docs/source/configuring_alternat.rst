Configuring alternat
====================

Alternat can be configured at a global generator level or at the driver level with settings related to individual driver.
We discuss configuration for both the generator and the driver for Application as well as Library mode below:


Configure Generator
-------------------------

Following configuration parameters are available for generator:

1. DEBUG:
    Setting the debug value to true will generate confidence level value for each of the OCR line
    detected by the system. In the debug output, it gives the line height and its ratio compared to the image height.
    This information is useful if you want to tune confidence level threshold value for drivers and
    OCR line height to image height ratio for filtering out insignificant text in the image.

2. ENABLE_OCR_CLUSTERING:
    Alternat comes with its own clustering rule
    which clusters (blobs) OCR data to create final OCR text from it. This is enabled by
    default and can be disabled by setting this value to false.

|

**Application Mode:**

You can find sample configuration for all the three drivers namely: opensource, azure, and google
under “path-to-repo/sample/generator_driver_conf/<drivername>.json”.
Inside the JSON file you will find the following configuration parameter:
GENERATOR: {DEBUG: false, ENABLE_OCR_CLUSTERING: true}

Here is an example to use the generator configuration for driver with name <drivername>:

.. code-block:: bash

    python app.py generate --output-dir-path="results" --input-image-file-path="sample/images_with_text/sample1.png" --driver-config-file-path="sample/generator_driver_conf/<drivername>.json"

Where <drivername> is the name of the driver (opensource, azure or google)

Based on the setting for DEBUG and ENABLE_OCR_CLUSTERING in
the sample/generator_driver_conf/<drivername>.json file the above
command will generate the result and dump it inside “results” folder.

|

**Library Mode:**

In Library mode, you can directly interact with alternat library API to set the
generator level config via a json object. Following is an example that will walk you
through the same:

Once you have setup the alternat using “pip install alternat” you can open the python shell
and run these commands to set generator config

.. code-block:: bash

      # import the Generator library
      from alternat.generation import Generator

      # instantiate the Generator for opensource driver (you can pass “azure” or
      # “google” when instantiating to the let the library know the driver you want
      # to use.
      generator = Generator()

      # get the current generator settings
      # This will return the existing configuration
      # {'DEBUG': False, 'ENABLE_OCR_CLUSTERING': True}
      generator.get_config()

      # set debug to true
      generator_config = {“DEBUG”: True}
      generator.set_config(generator_config)

      # or disable OCR clustering
      generator_config = {“ENABLE_OCR_CLUSTERING”: False}
      generator.set_config(generator_config)

      # or set values for both the parameters in one go
      generator_config = {“DEBUG”: True, “ENABLE_OCR_CLUSTERING”: False}
      generator.set_config(generator_config)

      # run generator over an image and dump the output inside “results” folder
      # this will run with DEBUG=true.
      generator.generate_alt_text_from_file("sample/images_with_text/sample1.png", "results")


Configure Driver
-------------------------

Generator comes with 3 drivers:

1. Opensource:
    Use EasyOCR for generating OCR text. This should be used when there is
    text in the image as it only has support for OCR at the moment.
    This is the default driver for generator, does not require any kind of registration and is free to use.

2. Azure:
    Uses Azure computer vision API to describe an image, generate OCR and also provide labels
    to the image. To use this driver, you need to register for computer vision API from Microsoft
    which will give you the SUBSCRIPTION_KEY and ENDPOINT URL to access the API.

3. Google:
    Uses Google computer vision API to generate OCR and provide labels to the image.
    To use this driver, you need to register for google computer vision API,
    download the google cloud service credentials file on your system and set the path to it
    in the driver configuration parameter ABSOLUTE_PATH_TO_CREDENTIAL_FILE (will be discussed below)

|

The following generator driver settings are available:

1. CAPTION_CONFIDENCE_THRESHOLD:
    Decimal based threshold to filter out caption data.
    For example, if you only want captions with confidence level above say 70%, then set this value to 0.70.
    This is most useful when using “azure” driver as Microsoft compute vision API has support for describing an image.

2. OCR_CONFIDENCE_THRESHOLD:
    Decimal based threshold to filter out OCR data.
    For example, if you want OCR text with confidence level about say 50%, then set this value to 0.50.

3. LABEL_CONFIDENCE_THRESHOLD:
    Decimal based threshold to filter out label data.
    For example, if you want labels with confidence level about say 80%, then set this value to 0.80.
    This is useful when using google and azure driver as both the APIs have support for labelling image.

4. OCR_HEIGHT_RATIO_TO_IMAGE_THRESHOLD:
    Decimal based threshold to filter out OCR text which does not
    occupy a major portion of image and is practically irrelevant even if detected by the system.
    This threshold considers the ratio of the height of the text and the image to decide whether the text
    needs to be filtered out or not. For example, if you want OCR data only when the line height is greater
    than let's say 1.5% then set this value to 0.015 in the config.

5. SUBSCRIPTION_KEY:
    This is the subscription key for azure computer vision API, and is only required
    when using **azure** as the driver.

6. ENDPOINT:
    This is the API endpoint URL for azure computer vision API, and is only required
    when using **azure** as the driver.

7. AZURE_RATE_LIMIT_ON:
    This enables rate limiting when using azure driver in free account.
    Azure has a limit of 30 requests / minute in free tier account and when running alternat over a
    set of images this limit can hit very quickly. Alternat avoids this by sleeping for 30 sec by default
    and trying again. This setting is enabled by default. This setting is only required when using **azure**
    as the driver.

8. AZURE_RATE_LIMIT_TIME_IN_SEC:
    This is the rate limit time in sec. Alternat will sleep for these
    many seconds (30 by default) when azure rate limiting is reached in free tier account.
    To increase the sleep timer from 30 to say 40 seconds, set the value of this parameter to 40.
    This setting is only required when using **azure** as the driver.

9. ABSOLUTE_PATH_TO_CREDENTIAL_FILE:
    This setting holds the absolute path to the
    google credentials file (required to access the Google cloud services and computer vision API).
    This setting is only required when using **google** as the driver.

|

Let's see how to configure the above parameters in both the application and library mode.

**Application Mode:**

You can find sample configuration for all the three drivers namely: opensource, azure, and google
under “path-to-repo/sample/generator_driver_conf/<drivername>.json”.
Inside the configuration file, you find all the parameters above with default values already set.
To change these values and run generator use the following command:

.. code-block:: bash

    python app.py generate --output-dir-path="results" --input-image-file-path="sample/images_with_text/sample1.png" --driver-config-file-path="sample/generator_driver_conf/<drivername>.json"

Where <drivername> is the name of the driver (opensource, azure or google)

|

**Library Mode:**

Once you have setup the alternat using “pip install alternat” you can open the python shell
and run these commands to set generator config:

.. code-block:: bash

    # import the Generator library
    from alternat.generation import Generator

    # instantiate the Generator for opensource driver (you can pass “azure” or
    # “google” when instantiating to the let the library know the driver you want
    # to use.

    # for opensource
    generator = Generator()

    # or for azure
    generator = Generator(“azure”)

    # or for google
    generator = Generator(“google”)

    # get the current generator driver settings
    # This will return the existing configuration based on the driver
    generator.get_driver_config()

    # set threshold value for caption, OCR and label
    generator_driver_config = {"CAPTION_CONFIDENCE_THRESHOLD": 0.2, "OCR_CONFIDENCE_THRESHOLD": 0.3, "LABEL_CONFIDENCE_THRESHOLD":0.75}
    generator. generator.set_driver_config (generator_driver_config)

    # or set OCR_HEIGHT_RATIO_TO_IMAGE_THRESHOLD
    generator_driver_config = {"OCR_HEIGHT_RATIO_TO_IMAGE_THRESHOLD":0.015}
    generator. generator.set_driver_config (generator_driver_config)

    # or set subscription key and endpoint URL for azure
    generator_driver_config = {"SUBSCRIPTION_KEY": "yoursubscriptionkey", "ENDPOINT":"https://<ENTER_PROJECT_NAME>.cognitiveservices.azure.com/"}
    generator. generator.set_driver_config (generator_driver_config)

    # run generator over an image and dump the output inside “results” folder
    # this will run with DEBUG=true.
    generator.generate_alt_text_from_file("sample/images_with_text/sample1.png", "results")
