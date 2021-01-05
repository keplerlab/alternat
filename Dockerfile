# This image was inspired by https://github.com/GoogleChrome/puppeteer/blob/master/docs/troubleshooting.md#running-puppeteer-in-docker
# Base Image
FROM continuumio/miniconda3 AS build

# Install dependencies and tools
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \
    wget \
    curl \
    libssl-dev \
    build-essential \
    apt-utils \
    zip \
    unzip \
    gcc \
    locales \
    nano \
    && apt-get clean

COPY ./setup_scripts/alternat.yml .
RUN conda env create --name alternat --file=alternat.yml

SHELL ["/bin/bash", "-c"]
# Install sphinx doc dependencies
RUN source activate alternat && pip install sphinx_js sphinx_rtd_theme
# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n alternat -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack


# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM debian:buster AS runtime

# Copy /venv from the previous stage:
COPY --from=build /venv /venv
SHELL ["/bin/bash", "-c"]

RUN apt-get update
RUN apt-get install -y wget gnupg curl procps build-essential ffmpeg libsm6 libxext6
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 --no-install-recommends
RUN rm -rf /var/lib/apt/lists/*


# node installation
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
ENV NODE_VERSION=12.18.0
RUN . ~/.nvm/nvm.sh
RUN . ~/.profile
RUN . ~/.bashrc

RUN [[ -s $HOME/.nvm/nvm.sh ]] && . $HOME/.nvm/nvm.sh && nvm install ${NODE_VERSION}
RUN [[ -s $HOME/.nvm/nvm.sh ]] && . $HOME/.nvm/nvm.sh && nvm use ${NODE_VERSION}
RUN mkdir -p ~/.alternat
RUN chown -R $(whoami) ~/.alternat
RUN [[ -s $HOME/.nvm/nvm.sh ]] && . $HOME/.nvm/nvm.sh && cd ~/.alternat && npm install apify --unsafe-perm=true
RUN [[ -s $HOME/.nvm/nvm.sh ]] && . $HOME/.nvm/nvm.sh && npm install -g jsdoc

#COPY ./setup_scripts/install_apify_ubuntu.sh .
#RUN sh install_apify_ubuntu.sh

# Arguments that can be set with docker build
ARG HOME_DIR=/usr/local/alternat

# Export the environment variable AIRFLOW_HOME where airflow will be installed
ENV ALTERNAT_HOME=${HOME_DIR}

#RUN npm install -g jsdoc

# Set workdir (it's like a cd inside the container)
WORKDIR ${ALTERNAT_HOME}
ENV PYTHONPATH "${PYTHONPATH}:/usr/local/alternat"
ENV OUTPUT_FOLDER "./DATADUMP/"

# Sets path to Chrome executable, this is used by Apify.launchPuppeteer()
ENV APIFY_CHROME_EXECUTABLE_PATH=/usr/bin/google-chrome

# Tell Node.js this is a production environemnt
#ENV NODE_ENV=production
# Enable Node.js process to use a lot of memory (actor has limit of 32GB)
# Increases default size of headers. The original limit was 80kb, but from node 10+ they decided to lower it to 8kb.
# However they did not think about all the sites there with large headers,
# so we put back the old limit of 80kb, which seems to work just fine.
ENV NODE_OPTIONS="--max_old_space_size=30000 --max-http-header-size=80000"
ENV APIFY_LOCAL_STORAGE_DIR="/usr/local/alternat/alternat/collection/apify/apify_storage"

# Pre download EasyOCR Model
RUN source /venv/bin/activate && (echo "import easyocr" ; echo "reader = easyocr.Reader(['en'])" ) | python


# Pre download caption model
COPY alternat /usr/local/alternat/alternat
COPY sample/images_with_text/sample1.png /usr/local/alternat/sample/images_with_text/sample1.png
RUN source /venv/bin/activate  && cd ${ALTERNAT_HOME} && (echo "from alternat.generation import Generator" ; echo "generator = Generator()" ; echo "generator.generate_alt_text_from_file('sample/images_with_text/sample1.png', 'results')" ) | python

RUN echo "source /venv/bin/activate" >> ~/.bashrc
# Expose ports (just to indicate that this container needs to map port)
EXPOSE 8080
ENV SHELL /bin/bash
# Execute the entrypoint.sh
ENTRYPOINT ["bash", "./setup_scripts/entrypoint.sh" ]

