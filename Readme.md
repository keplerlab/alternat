## **alternat**: Automate your image alt-text generation workflow.

![](logo.png)
### Resources 
* Homepage and Reference: <https://alternat.readthedocs.io/>

### Description
alternat automates the image alt-text generation workflow by offering ready to use methods for downloading (Collection in alternat lingo) images and then generating alt-text.

alternat features are grouped into tasks - Collection and Generation

**Collection**

Collection offers convenience methods to download images. It uses puppeteer (headless chrome) to automate the website crawling and image download process  

**Generation**

Generation offers convenience methods to generate alt-texts. It offers drivers to generate the alt-texts.
1. Azure API - Uses Azure API for image captioning and OCR. Note Azure is a paid service.
2. Google API - Uses google API for image captioning and OCR. Note google is a paid service.
3. Open Source - Uses free open source alternative for OCR and image captioning.

**Supported Video and image file formats**
jpeg, jpg and png are supported.

## Installation

### Installation using Docker
1. Download and Install Docker Desktop for Mac using this link [docker-desktop](https://www.docker.com/products/docker-desktop)

2. Clone this repo https://github.com/keplerlab/alternat.git 

3. Change your directory to your cloned repo.

4. Open terminal and run following commands
```
cd <path-to-repo> //you need to be in your repo folder
docker-compose build
```
5. Start docker container using this command
```
docker-compose up
```
6. In a new terminal window open terminal inside docker container for running alternat using command line type following command:
```
docker-compose exec alternat bash
```

7. You can use this command line to execute collect or generate command line application like [this](https://alternat.readthedocs.io/en/main/using_alternat.html#application-mode-via-cli-command-line-interface) . 


### Installation from pypi, source and Anaconda Python

Please refer to os specific respective installation guides for [macOS](https://alternat.readthedocs.io/en/main/installation/installing_alternat_macos.html), [ubuntu](https://alternat.readthedocs.io/en/main/installation/installing_alternat_ubuntu.html) and 
[Windows](https://alternat.readthedocs.io/en/main/installation/installing_alternat_windows.html) respectively. 

## Running generate task using command line:

If you want to generate alternate text for any image or folder containing 
multiple images, you can use Command line option which we call generation stage. 

To run generation stage alone you can use following command: 

```
# To run a single file, results will be collected under "results/generate"
# The image extensions supported are: .jpg, .jpeg, .png.

python app.py generate --output-dir-path="./results" --input-image-file-path="./sample/images_with_text/sample1.png"  

or

# To run for entire directory, results will be collected under "results/generate"
# The image extensions supported are: .jpg, .jpeg, .png.

python app.py generate --input-dir-path="./sample/images_with_text" --output-dir-path="./results"

or 

# To generate alt-text using specific driver (like azure, google or open source)
# Do not forget to add the credentials to their respective config files when using azure and google
# azure needs SUBSCRIPTION_KEY and ENDPOINT URL
# google needs ABSOLUTE_PATH_TO_CREDENTIALS_FILE (a credential json file)

python app.py generate --output-dir-path="./results" --input-image-file-path="./sample/images_with_text/sample1.png" --driver-config-file-path="./sample/generator_driver_conf/azure.json"

```


Sample images are located at sample/images and sample/images_with_text

## Running collect task using command line:
First stage is called collection stage, it can be used to crawl and download images from any website or website url, to run the collection stage use following commands:

### Use case: Download image from single page 
```bash
    # To run the collection 
     python app.py collect  --url=<WEBSITE_URL> --output-dir-path=./DATADUMP
```

### Use case: Download images recursively for a given site

```bash
    # To run the collection 
    python app.py collect --download-recursive --url=<WEBSITE_URL> --output-dir-path=./DATADUMP
```


## Knows Issue / Troubleshooting

Please refer to [FAQ\Troubleshooting section](https://alternat.readthedocs.io/en/main/faq.html) inside alternat documenation, or raise 
an Github issue. 

### Attributions
1. For open source ocr we are using EasyOCR project https://github.com/JaidedAI/EasyOCR by Rakpong Kittinaradorn.
2. For opensource caption generation we are using model training and inference scripts using method at https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Image-Captioning by Sagar Vinodababu. 
3. For web crawling we are using apify wrapper over puppeteer library https://apify.com/. 

