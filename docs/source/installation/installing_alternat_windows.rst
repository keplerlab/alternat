Installing alternat windows 
============================

Install using pypi (Windows)
-----------------------------

1. Install Node (>=v.12)

2. Install Python (>=3.8)

3. Install apify by first downloading install_from_pypi_windows.bat script 
located at setup_scripts folder in alternat repo 
[link](https://github.com/keplerlab/alternat/blob/main/setup_scripts/install_from_pypi_windows.bat) 
and then executing downloaded script inside new windows powershell prompt::

    .\install_from_pypi_windows.bat


Install from source (Windows)
------------------------------

1. Install git

2. Install Node (>=v.12)

3. Install Python (>=3.8)

4. Open terminal and clone the repo

    git clone https://github.com/keplerlab/alternat.git

5. Change the directory to the directory where you have cloned your repo ::

    $cd path_to_the_folder_repo_cloned

6. Install apify by executing given script inside windows powershell prompt::
        
    cd setup_scripts 
    .\install_from_source_windows.bat




Installation using Anaconda python (Windows)
----------------------------------------------

1. Install git

2. Install Node (>=v.12)

3. Install Python (>=3.8)

4. Open terminal and clone the repo inside windows powershell prompt::

    git clone https://github.com/keplerlab/alternat.git

5. Change the directory to the directory where you have cloned your repo ::

    $cd path_to_the_folder_repo_cloned


6. Create conda environment and install dependencies using
   enviorment_windows.yml file ::

    cd setup_scripts
    conda env create --name alternat --file=alternat_env_windows.yml

7. Activate newly created environment::

    conda activate alternat

8. Install apify by executing given script inside windows powershell promp::
        
    cd setup_scripts
    .\install_apify_windows.bat



Installation using Docker (Windows)
------------------------------------

1. Download and Install Docker Desktop for Mac using link: https://docs.docker.com/docker-for-mac/install/

2. Clone this repo

3. Change your directory to the cloned repo.

4. Open terminal and run following commands::

    cd <path-to-repo> //you need to be in your repo folder
    docker-compose build

5. Start docker container using this command inside windows powershell or cmd promp::

    docker-compose up

6. In a new windows powershell or cmd window open terminal and enter into alternat docker container using command::

    docker-compose exec alternat bash
