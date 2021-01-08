Installing alternat macOS
==========================

Install using pypi (macOS)
----------------------------

1. Install Node (>=v.12)

2. Install Python (>=3.8)

3. Install alternat::

    pip install alternat

4. Install apify ::

    mkdir -p ~/.alternat && cd ~/.alternat && npm install apify && cd -


Install from source (macOS)
-----------------------------

1. Install git

2. Install Node (>=v.12)

3. Install Python (>=3.8)

4. Open terminal and clone the repo::

    git clone https://github.com/keplerlab/alternat.git

5. Change the directory to the directory where you have cloned your repo ::

    $cd path_to_the_folder_repo_cloned

6. Install apify ::
  
    mkdir -p ~/.alternat && cd ~/.alternat && npm install apify && cd -

7. Install alternat using setup.py ::

    python setup.py install 


Installation using Anaconda python (macOS)
-------------------------------------------

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

8. Install apify ::

    mkdir -p ~/.alternat && cd ~/.alternat && npm install apify && cd -


Installation using Docker (macOS)
----------------------------------

1. Download and Install Docker Desktop for Mac using link: https://docs.docker.com/docker-for-mac/install/

2. Clone this repo

3. Change your directory to the cloned repo.

4. Open terminal and run following commands::

    cd <path-to-repo> //you need to be in your repo folder
    docker-compose up

5. In a new terminal window open terminal and enter into alternat docker container using command::

    docker-compose exec alternat bash
