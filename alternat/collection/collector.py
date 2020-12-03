import shutil
import os
import subprocess
import sys
import pathlib


class Collector:

    def __init__(self):
        """
        """

    def process(
        self,
        url: str,
        output_dir_path: str,
        download_recursive: bool = False,
        collect_using_apify: bool = False,
    ):
        """Collects image from the url into the output directory

        :param url: [description]
        :type url: str
        :param output_dir_path: [description]
        :type output_dir_path: str
        :param download_recursive: [description], defaults to False
        :type download_recursive: bool, optional
        :param collect_using_apify: [description], defaults to False
        :type collect_using_apify: bool, optional
        """
        startURLArg = "start_urls=" + url
        try:
            os.environ["DOWNLOAD_URL"] = url
            os.environ["OUTPUT_FOLDER"] = output_dir_path
            if not os.path.exists(output_dir_path):
                os.makedirs(output_dir_path)
            if not collect_using_apify:
                print("No crawler explicitly mentioned, using default apify crawler")
                collect_using_apify = True
            if collect_using_apify:
                # Get directory name
                apify_storage_dir = os.path.join(".", "apify_storage")
                current_dir = pathlib.Path(__file__).parent.absolute()
                node_folder_path = os.path.join(os.path.expanduser("~"), ".alternat", "node_modules")
                os.environ["NODE_PATH"] = node_folder_path
                os.environ["APIFY_LOCAL_STORAGE_DIR"] = apify_storage_dir
                ## Try to remove tree; if failed show an error using try...except on screen
                try:
                    shutil.rmtree(apify_storage_dir)
                except OSError as e:
                    print ("Error: %s - %s." % (e.filename, e.strerror))
                if download_recursive:
                    # TODO remove slash to os.path
                    # TODO remove path to current file
                    script_path = os.path.join(current_dir, "apify", "main.js")
                    output = subprocess.check_output(["node", script_path,])
                else:
                    print(f"Downloading single page", url)
                    script_path = os.path.join(current_dir, "apify", "main_single_page.js")
                    output = subprocess.check_output(["node", script_path,])
                # TODO Remove print statement 
                #print("output", output, flush=True)
            else:
                print("Set at least collect-using-apify or collect-using-scrapy to True")

        except subprocess.CalledProcessError as e:
            print("\n Subprocess error")
            print(str(e.output))
        except Exception as e:
            print("\n\n\nException occurred doing cleanup\n\n\n")
            print(e)
            raise
