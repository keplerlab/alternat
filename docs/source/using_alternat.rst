Using alternat
==============

Application Mode via CLI (Command Line Interface)
-----------------------------------------------------

Alternat comes with a python-based CLI app **app.py** which provides commands to run collection and generation task.
Below we give some example on how to use this app:


Collection:

1. Collect and store images from a URL and store them in a folder sample/images/test
    .. code-block:: bash

      python app.py collect --url=”https://page_url” --output-dir-path="sample/images/test"

2. Collect and store the images from a URL **recursively** and store them in a folder sample/images/test
    .. code-block:: bash

      python app.py collect --url=”https://page_url” --output-dir-path="sample/images/test" --download-recursively=true

|

Generation

1. Generate alt-text for the images in a directory name sample/images_with_text and save data in directory structure results:
    .. code-block:: bash

      python app.py generate --input-dir-path=”sample/images_with_text” --output-dir-path=”results”


2. Generate alt-text for a single image in a folder sample/images_with_text and save its result in a directory inside results:
    .. code-block:: bash

      python app.py generate --input-image-file-path=”sample/images_with_text/sample1.png” --output-dir-path=”results”

3. Generate alt-text based on user defined (custom) config for driver azure :
    .. code-block:: bash

      python app.py generate --input-image-file-path=”sample/images_with_text/sample1.png” --output-dir-path=”results” --driver-config-file-path=”sample/generator_driver_conf/azure.json”

    The above command can be changed based on the driver by using the driver
    sample files under sample/generator_driver_conf. For example, to use google driver
    change the –driver-config-file-path to “sample/generator_driver_conf/google.json”.


Library Mode
-------------------------

With library mode, users can integrate alternat in their existing applications as well.
In library mode the package is installed via pip and can be import into python applications directly.
Below are some examples on using the library mode for collection and generation tasks:

Collection:

Download the image from a site given its URL to specified folder location:

    .. code-block:: bash

      # import the alternat library
      from alternat.collection import Collector

      # instantiate the collector
      collector = Collector()

      # Download images from url and saves image files in  output_dir_path
      # Optional parameters, download_recursive if True crawls whole site mentioned in
      # url by visiting each link recursively and downloads images
      # collect_using_apify in future more crawlers will be supported this parameter
      # ensures that apify crawler is used.
      collector.process(url, output_dir_path, download_recursive, collect_using_apify

    |

Generator:

1. Generate alt-text for a single image in a folder "results" and save its result in a directory inside result/test:
    .. code-block:: bash

      # import the Generator
      from alternat.generation import Generator

      # instantiate the generator (uses opensource driver by default)
      generator = Generator()

      # to use a specific driver pass the driver name when instantiating. For e.g, to use
      # azure driver use
      generator = Generator(“azure”)

      # generate the alt text
      generator.generate_alt_text_from_file("sample/images_with_text/sample1.png", "results")

2. Generate alt-text for a single image in base64 image:
    .. code-block:: bash

      # import the Generator
      from alternat.generation import Generator

      # instantiate the generator (uses opensource driver by default)
      generator = Generator()

      # generate the alt text
      base64_image_str = "base64-image-data-here"
      generator.generate_alt_text_from_base64(base64_image_str)



Service Mode
--------------------

Generation:
    .. code-block:: bash

      # Go to api folder

      # run this command to start the service
      uvicorn message_processor:app --port 8080 --host 0.0.0.0 --reload 2>&1 | tee -a log.txt

    # send a post request with base64 image to the REST Server

    URL: http://localhost:8080/generate_text_base64

    body: { base64: “base64_image_str”}
