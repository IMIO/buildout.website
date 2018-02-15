FROM docker-staging.imio.be/base:latest
RUN mkdir /home/imio/imio-website
COPY *.cfg /home/imio/imio-website/
COPY Makefile /home/imio/imio-website/
COPY *.py /home/imio/imio-website/
COPY scripts /home/imio/imio-website/scripts
RUN chown imio:imio -R /home/imio/imio-website/
WORKDIR /home/imio/imio-website
RUN apt-get -qy update && apt-get -qy install \
    build-essential \
    gcc \
    libjpeg-dev \
    libxml2-dev \
    libxslt1-dev \
    lynx \
    poppler-utils \
    python \
    python-dev \
    wget \
    wv \
    zlib1g-dev
USER imio
RUN make buildout-cache/downloads &&\
    /usr/bin/python bootstrap.py -c docker.cfg &&\
    make buildout-docker
USER root
RUN apt-get remove -y gcc python-dev &&\
    apt-get autoremove -y &&\
    apt-get clean
USER imio
ENV HOME /home/imio/imio-website
ENV ZEO_HOST db
ENV ZEO_PORT 8100
ENV HOSTNAME_HOST local
ENV PROJECT_ID imio
