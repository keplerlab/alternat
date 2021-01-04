import typer
from typing import Optional
import os
import sys
import json

from alternat.generation import Generator
from alternat.generation.exceptions import InvalidConfigFile, InvalidGeneratorDriver
from alternat.collection import Collector
import subprocess
import shutil

app = typer.Typer()

# This key determines the driver (if present in the json file)
_DRIVER_KEY = "DRIVER"

# This key determines the generator level config (if present in the json file)
_GENERATOR_KEY = "GENERATOR"


@app.command("collect")
def collect(
    url: str,
    output_dir_path: str,
    download_recursive: bool = False,
    collect_using_apify: bool = True,
):
    """Collects image from URL specified.

    :param url: The URL from where the image needs to be downloaded.
    :type url: str
    :param output_dir_path: Path to directory where the images downloaded should be dumped
    :type output_dir_path: str
    :param download_recursive: Whether to recursively crawl a site, defaults to False
    :type download_recursive: bool, optional
    :param collect_using_apify: Whether to crawl using appify crawler, defaults to True
    :type collect_using_apify: bool, optional
    """
    collector = Collector()
    collector.process(url, output_dir_path, download_recursive, collect_using_apify)


@app.command("generate")
def generate(
    output_dir_path: str = typer.Option(...),
    input_dir_path: str = None,
    input_image_file_path: str = None,
    base64_image: str = None,
    driver_config_file_path: str = None

):
    """Analyze the image to generate alt-text
    
    :param output_dir_path: Output dir path to store the results, defaults to typer.Option(...)
    :type output_dir_path: str, optional
    :param input_dir_path: Directory path to the folder containing images, defaults to None
    :type input_dir_path: str, optional
    :param input_image_file_path: Path to image file to be processed (used only if single image needs to be processed), defaults to None
    :type input_image_file_path: str, optional
    :param base64_image: Base64 image to be processed (used only if single image needs to be processed), defaults to None
    :type base64_image: str, optional
    :param driver_config_file_path: Path to the generator JSON config file (defaults will be used if not provided)
    :return:, defaults to None
    :type driver_config_file_path: str, optional
    :raises InvalidGeneratorDriver: Driver invalid error.
    :raises InvalidConfigFile: Configuration file is invalid.
    :return: collection of JSON representing alt-text data for images
    :rtype: [type]
    """
    generator = Generator()

    if driver_config_file_path is not None:
        file_extension = driver_config_file_path.split(".")[-1]
        if file_extension.lower() == "json":

            #read the json file
            with open(driver_config_file_path) as f:
                data = json.load(f)

                if _DRIVER_KEY in data.keys():
                    generator = Generator(data[_DRIVER_KEY])
                    generator.set_driver_config(data)
                else:
                    raise InvalidGeneratorDriver(Generator.ALLOWED_DRIVERS)

                # check if generator conf is present
                if _GENERATOR_KEY in data.keys():
                    generator_conf = data[_GENERATOR_KEY]
                    generator.set_config(generator_conf)
        else:
            raise InvalidConfigFile()

    results = []
    if input_dir_path is None:
        if input_image_file_path is None:

            if base64_image is not None:
                result_json = generator.generate_alt_text_from_base64(base64_image)
                print(result_json)
                return result_json
            else:
                typer.echo("One of --base64_image or --input-image-file-path is missing")
                return
        else:
            typer.echo("Processing image : %s" % input_image_file_path)

            result_json = generator.generate_alt_text_from_file(input_image_file_path, output_dir_path)
            print(result_json)
            return result_json
    else:
        for path, subdirs, files in os.walk(input_dir_path):
            for filename in files:
                if (
                    filename.endswith(".jpg")
                    or filename.endswith(".png")
                    or filename.endswith(".jpeg")
                ):
                    image_path = os.path.join(path, filename)
                    typer.echo("Processing image : %s" % image_path)
                    result_json = generator.generate_alt_text_from_file(image_path, output_dir_path)
                    print(result_json)
                    results.append(result_json)
                    typer.echo("Result saved at : %s" % output_dir_path)

        return results


if __name__ == "__main__":
    app()
