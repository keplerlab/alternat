Installing alternat
===================

Install using pypi
--------------------

1. Install Node (>=v.12)

2. Install Python (>=3.8)

3. Install alternat

    .. code-block:: bash

      pip install alternat

4. Install apify at alternat designated folder

    .. code-block:: bash

      # For ubuntu / linux run this command before installing apify
      sudo apt-get install -y procps  libxss1 fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf ffmpeg libsm6 libxext6

      mkdir -p ~/.alternat && cd ~/.alternat && npm install apify && cd -



Install from source
-------------------------

1. Install git

2. Install Node (>=v.12)

3. Install Python (>=3.8)

4. Open terminal and clone the repo

    .. code-block:: bash

      git clone https://github.com/keplerlab/alternat.git

5. Run the setup if alternat is to be used as a standalone application (for mac and linux only)

    .. code-block:: bash

      sh install_application_mode.sh

5. Run the setup if alternat is to be used as a service exposed over http.

    .. code-block:: bash

      sh install_api_mode.sh


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
