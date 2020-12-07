## **alternat**: Automate your image alt-text generation workflow.
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
3. Open Source - Uses free open source alternative for OCR.

**Supported Video and image file formats**
jpeg, jpg and png are supported.

## Installation

### Using pypi

1) Install node (>=v.12)
2) Install Python >= 3.8 
3) pip install alternat

Note 1: for Windows, please install torch and torchvision first by following the official instruction here https://pytorch.org. On pytorch website, be sure to select the right CUDA version you have. If you intend to run on CPU mode only, select CUDA = None. Or use Docker compose for running instructions [here](https://alternat.readthedocs.io/en/main/installing_alternat.html#installation-using-docker)

4) Install apify at alternat designated folder

For Windows go to setup_scripts and execute batch script

```
install_apify_window.bat 
```

For Ubuntu/Linux goto setup_scripts and execute bash script
```
sudo sh install_apify_ubuntu.sh
```

For Mac execute following command
```bash
mkdir -p ~/.alternat && cd ~/.alternat && npm install apify && cd -
```
      


### Install from source
1) Install git
2) Install node (>=v.12)
3) Install python >= 3.8
4) Open terminal or command prompt 
5) Clone repo from here https://github.com/keplerlab/alternat.git 
6) Change the directory to the directory where you have cloned your repo 
    ```
    $cd path_to_the_folder_repo_cloned
    ```
7) Install apify at alternat designated folder

For Windows goto setup_scripts and execute batch script

```
install_apify_window.bat 
```

For Ubuntu/Linux goto setup_scripts and execute bash script
```
sudo sh install_apify_ubuntu.sh
```

For Mac execute following command
```bash
mkdir -p ~/.alternat && cd ~/.alternat && npm install apify && cd -
```

8) Go to setup_scripts folder and run the setup if alternat to be used as standalone application:
``` 
    sh install_application_mode.sh 
```

   Run the setup if alternat to be used as service:
``` 
    sh install_api_mode.sh 
``` 

**Note**: For Windows run following batch files from setup_scripts folder instead of above bash scripts

``` 
    install_application_mode_windows.bat 
```

Run the setup if alternat to be used as service:
``` 
    install_api_mode_windows.bat
``` 



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

### Installation using Anaconda python

1. Install node (>=v.12) 
2. Create conda environment and install dependencies using environment.yml file

```
conda env create -f environment.yml
```

For windows use environment_windows.yml file for conda env create

```
conda env create -f environment_windows.yml
```

3. If you want to do image downloads from websites (collect step in alternat) using apify pupeeter you need to also first install nodejs and then goto folder apify. Run npm install:
```
cd <repo_path>
cd alternat/collection/apify
npm install
```

4. Install apify at alternat designated folder

For Windows goto setup_scripts and execute batch script

```
install_apify_window.bat 
```

For Ubuntu/Linux goto setup_scripts and execute bash script
```
sudo sh install_apify_ubuntu.sh
```

For Mac execute following command
```bash
mkdir -p ~/.alternat && cd ~/.alternat && npm install apify && cd -
```


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
    python app.py collect --collect-using-apify <WEBSITE_URL> ./DATADUMP
```

### Use case: Download images recursively for a given site

```bash
    # To run the collection 
    python app.py collect --collect-using-apify --download-recursive <WEBSITE_URL> ./DATADUMP
```



## Knows Issue / Troubleshooting

1. If you get error like **Error: spawn wmic.exe ENOENT** while running collect command (using apify) in alternat on **Microsoft Windows** 
This indicates that the wmic utility's directory is not found on your PATH. Open the advanced System Properties window (you can open the System page with Windows+Pause/Break) and on the Advanced tab, click Environment Variables. In the section for system variables, find PATH (or any capitalization thereof). Add this entry to it:
```
%SystemRoot%\System32\Wbem
```
Note that entries are delimited by semicolons.

### Attributions
1. For open source ocr we are using EasyOCR project https://github.com/JaidedAI/EasyOCR by Rakpong Kittinaradorn.
2. For web crawling we are using apify wrapper over puppeteer library https://apify.com/. 
