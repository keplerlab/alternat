Installing alternat
===================

Install using pypi
--------------------

1. Install Node (>=v.12)

2. Install Python (>=3.8)

3. Install alternat

    .. code-block:: bash

      pip install alternat

Note 1: for Windows, please install torch and torchvision first by following the official instruction here https://pytorch.org.
On pytorch website, be sure to select the right CUDA version you have.
If you intend to run on CPU mode only, select CUDA = None. Or use Docker compose
for running instructions [here](https://alternat.readthedocs.io/en/main/installing_alternat.html#installation-using-docker)


4. Install apify at alternat designated folder

For Windows go to setup_scripts and execute batch script ::

    install_apify_window.bat 



For Ubuntu/Linux goto setup_scripts and execute bash script ::

    sudo sh install_apify_ubuntu.sh


For Mac execute following command ::

      mkdir -p ~/.alternat && cd ~/.alternat && npm install apify && cd -


Install from source
-------------------------

1. Install git

2. Install Node (>=v.12)

3. Install Python (>=3.8)

4. Open terminal and clone the repo

    .. code-block:: bash

      git clone https://github.com/keplerlab/alternat.git

5. Change the directory to the directory where you have cloned your repo ::

    $cd path_to_the_folder_repo_cloned

6. Install apify at alternat designated folder

For Windows goto setup_scripts and execute batch script ::

    install_apify_window.bat 

For Ubuntu/Linux goto setup_scripts and execute bash script::

    sudo sh install_apify_ubuntu.sh

For Mac execute following command ::
  
    mkdir -p ~/.alternat && cd ~/.alternat && npm install apify && cd -
7. Go to setup_scripts folder and run the setup if alternat to be used as standalone application::

    sh install_application_mode.sh 

   Run the setup if alternat to be used as service::

    sh install_api_mode.sh 

**Note**: For Windows run following batch files from setup_scripts folder instead of above bash scripts::

    install_application_mode_windows.bat 

Run the setup if alternat to be used as service::

    install_api_mode_windows.bat



Installation using Docker
-------------------------

1. Download and Install Docker Desktop for Mac using link: https://docs.docker.com/docker-for-mac/install/

2. Clone this repo

3. Change your directory to the cloned repo.

4. Open terminal and run following commands

    .. code-block:: bash

      cd <path-to-repo> //you need to be in your repo folder
      docker-compose build

5. Start docker container using this command

    .. code-block:: bash

      docker-compose up

6. In a new terminal window open terminal and enter into alternat docker container using command:

    .. code-block:: bash

      docker-compose exec alternat bash


Installation using Anaconda python
----------------------------------

1. Install Node (>=v.12)

2. Create conda environment and install dependencies using
   environment.yml file

    .. code-block:: bash

      conda env create -f environment.yml

For windows use environment_windows.yml file for conda env create

    .. code-block:: bash

      conda env create -f environment_windows.yml

3. If you want to do image downloads from websites (collect step in alternat) using apify pupeeter you need to also first install nodejs and then goto folder apify. Run npm install::

    cd <repo_path>
    cd alternat/collection/apify
    npm install

4. Install apify at alternat designated folder

For Windows goto setup_scripts and execute batch script::

    install_apify_window.bat 

For Ubuntu/Linux goto setup_scripts and execute bash script::

    sudo sh install_apify_ubuntu.sh

For Mac execute following command::
    
    mkdir -p ~/.alternat && cd ~/.alternat && npm install apify && cd -
