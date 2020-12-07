# This image was inspired by https://github.com/GoogleChrome/puppeteer/blob/master/docs/troubleshooting.md#running-puppeteer-in-docker
# Base Image
FROM python:3.8-slim

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

ENV NODE_VERSION=12.18.0
ENV NVM_DIR=/usr/local/.nvm
RUN mkdir -p ${NVM_DIR}
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/usr/local/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

# Install latest Chrome dev packages and fonts to support major charsets (Chinese, Japanese, Arabic, Hebrew, Thai and a few others)
# Note: this also installs the necessary libs to make the bundled version of Chromium that Puppeteer installs, work.

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y wget gnupg unzip ca-certificates --no-install-recommends \
 && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | DEBIAN_FRONTEND=noninteractive apt-key add - \
 && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
 && DEBIAN_FRONTEND=noninteractive apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get purge --auto-remove -y wget unzip \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y procps git google-chrome-stable libxss1 fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf \
 ffmpeg libsm6 libxext6 \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/* \
 && rm -rf /src/*.deb \
 && rm -rf /opt/yarn /usr/local/bin/yarn /usr/local/bin/yarnpkg


# Arguments that can be set with docker build
ARG HOME_DIR=/usr/local/alternat

# Export the environment variable AIRFLOW_HOME where airflow will be installed
ENV ALTERNAT_HOME=${HOME_DIR}

COPY ./setup_scripts/requirements-python3.8.txt /requirements-python3.8.txt

RUN pip install --upgrade pip && \
#    useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow && \
    pip install scrapy typer treelib pillow google-cloud-vision tldextract typer fastapi uvicorn easyocr pyyaml sphinx_js sphinx_rtd_theme --constraint /requirements-python3.8.txt

RUN npm install -g jsdoc

# Set workdir (it's like a cd inside the container)
WORKDIR ${ALTERNAT_HOME}

RUN mkdir -p ${ALTERNAT_HOME}/alternat/collection/apify
COPY ./alternat/collection/apify/package.json ${ALTERNAT_HOME}/alternat/collection/apify
RUN cd ${ALTERNAT_HOME}/alternat/collection/apify && npm install && cd ..

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
RUN (echo "import easyocr" ; echo "reader = easyocr.Reader(['en'])" ) | python

# Expose ports (just to indicate that this container needs to map port)
EXPOSE 8080
ENV SHELL /bin/bash
# Execute the entrypoint.sh
ENTRYPOINT ["bash", "./setup_scripts/entrypoint.sh" ]

