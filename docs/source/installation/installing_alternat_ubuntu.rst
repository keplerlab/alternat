Installing alternat ubuntu 
===========================

Install using pypi (ubuntu)
-----------------------------

1. Install Node (>=v.12)

2. Install Python (>=3.8)

3. Install alternat::

    pip install alternat

4. Install apify by first downloading install_apify_ubuntu.sh located at 
setup_scripts folder in alternat `Repo link <https://raw.githubusercontent.com/keplerlab/alternat/main/setup_scripts/install_apify_ubuntu.sh>`_  and then executing downloaded script ::


    sudo sh install_apify_ubuntu.sh


Install from source (ubuntu)
------------------------------

1. Install git

2. Install Node (>=v.12)

3. Install Python (>=3.8)

4. Open terminal and clone the repo

    git clone https://github.com/keplerlab/alternat.git

5. Change the directory to the directory where you have cloned your repo ::

    $cd path_to_the_folder_repo_cloned

6. Install apify by executing given script ::
        
    cd setup_scripts 
    sudo sh install_apify_ubuntu.sh

7. Install alternat using setup.py ::

    python setup.py install 



Installation using Anaconda python (ubuntu)
--------------------------------------------

1. Install git

2. Install Node (>=v.12)

3. Install Python (>=3.8)

4. Open terminal and clone the repo::

    git clone https://github.com/keplerlab/alternat.git

5. Change the directory to the directory where you have cloned your repo ::

    $cd path_to_the_folder_repo_cloned


6. Create conda environment and install dependencies using
   alternat.yml file ::

    cd setup_scripts
    conda env create --name alternat --file=alternat.yml

7. Activate newly created environment::

    conda activate alternat

8. Install apify by executing given script ::
        
    cd setup_scripts
    sudo sh install_apify_ubuntu.sh



Installation using Docker (ubuntu)
-------------------------------------

1. Download and Install Docker Desktop for Mac using link: https://docs.docker.com/docker-for-mac/install/

2. Clone this repo

3. Change your directory to the cloned repo.

4. Open terminal and run following commands::

    cd <path-to-repo> //you need to be in your repo folder
    docker-compose up

5. In a new terminal window open terminal and enter into alternat docker container using command::

    docker-compose exec alternat bash
