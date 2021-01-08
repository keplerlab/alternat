# This image was inspired by https://github.com/GoogleChrome/puppeteer/blob/master/docs/troubleshooting.md#running-puppeteer-in-docker
# Base Image
FROM continuumio/miniconda3 AS build

# Install dependencies and tools
RUN DEBIAN_FRONTEND=noninteractive apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \
#    wget \
#    curl \
    libssl-dev \
    build-essential \
    apt-utils \
    zip \
    unzip \
    gcc \
    locales \
    nano \
    ffmpeg libsm6 libxext6 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /src/*.deb \
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

ENV EASYOCR_MODULE_PATH="/root/.alternat/"
# Pre download EasyOCR Model
RUN source /venv/bin/activate && (echo "import easyocr" ; echo "reader = easyocr.Reader(['en'])" ) | python
# Pre download caption model
COPY alternat /usr/local/alternat/alternat
COPY sample/images_with_text/sample1.png /usr/local/alternat/sample/images_with_text/sample1.png
RUN source /venv/bin/activate  && cd /usr/local/alternat/ && (echo "from alternat.generation import Generator" ; echo "generator = Generator()" ; echo "generator.generate_alt_text_from_file('sample/images_with_text/sample1.png', 'results')" ) | python

# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM apify/actor-node-chrome AS runtime
USER root
# Copy /venv from the previous stage:
COPY --from=build /venv /venv
COPY --from=build /root/.alternat /root/.alternat
SHELL ["/bin/bash", "-c"]

RUN DEBIAN_FRONTEND=noninteractive apt-get update &&\
DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg libsm6 libxext6 --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /src/*.deb 

# Set workdir (it's like a cd inside the container)
WORKDIR /home/myuser/alternat
ENV PYTHONPATH "${PYTHONPATH}:/home/myuser/alternat"

# EASYOCR_MODULE_PATH is the location where easyOCR expects model to be downloaded
ENV EASYOCR_MODULE_PATH="/root/.alternat/"
# apify will complain if following is not set
ENV APIFY_LOCAL_STORAGE_DIR="/home/myuser/alternat/alternat/collection/apify/apify_storage"
ENV OUTPUT_FOLDER "./DATADUMP/"

RUN echo "source /venv/bin/activate" >> ~/.bashrc
# Expose ports (just to indicate that this container needs to map port)
EXPOSE 8080
ENV SHELL /bin/bash
# Execute the entrypoint.sh
ENTRYPOINT ["bash", "./setup_scripts/entrypoint.sh" ]
