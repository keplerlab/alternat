import os
import sys
import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

analyze_url = endpoint + "vision/v3.1/ocr"

# Set image_path to the local path of an image that you want to analyze.
# Sample images are here, if needed:
# https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/ComputerVision/Images
dir_image_path = "/images_with_text"

for filename in os.listdir(dir_image_path):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".svg") or filename.endswith(".png"):
        x = input(" filename " + filename + ". Continue ? (y/n) ")

        if x.lower() == "y":
            file_path = os.path.join(dir_image_path, filename)
            # Read the image into a byte array
            image_data = open(file_path, "rb").read()
            headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                       'Content-Type': 'application/octet-stream'}
            params = {'language': 'en', 'detectOrientation': 'true'}

            try:
                response = requests.post(
                    analyze_url, headers=headers, params=params, data=image_data)
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                print(response.content)
                continue


            # The 'analysis' object contains various fields that describe the image. The most
            # relevant caption for the image is obtained from the 'description' property.
            analysis = response.json()
            print(analysis)
            # Extract the word bounding boxes and text.
            line_infos = [region["lines"] for region in analysis["regions"]]
            word_infos = []
            for line in line_infos:
                for word_metadata in line:
                    for word_info in word_metadata["words"]:
                        word_infos.append(word_info)
            word_infos

            # Display the image and overlay it with the extracted text.
            plt.figure(figsize=(5, 5))
            image = Image.open(BytesIO(image_data))
            print(" type of image ", type(image))
            ax = plt.imshow(image)
            for word in word_infos:
                bbox = [int(num) for num in word["boundingBox"].split(",")]
                text = word["text"]
                origin = (bbox[0], bbox[1])
                patch = Rectangle(origin, bbox[2], bbox[3],
                                  fill=False, linewidth=2, color='y')
                ax.axes.add_patch(patch)
                plt.text(origin[0], origin[1], text, fontsize=20, weight="bold", va="top")
            plt.show()
            plt.axis("off")
        else:
            print("Skipping")
