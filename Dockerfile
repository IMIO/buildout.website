FROM docker-staging.imio.be/base:latest
MAINTAINER Benoît Suttor <benoit.suttor@imio.be>
ARG repo=buildout.website
ARG cmd="make buildout"
# Pillow lib : libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN apt-get -qy update && apt-get -qy install \
    build-essential \
    gcc \
    git \
    libbz2-dev \
    libffi-dev \
    libjpeg62-dev \
    libreadline-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    lynx \
    poppler-utils \
    python-dev \
    python-pip \
    python-virtualenv \
    wv \
    zlib1g-dev

USER imio
WORKDIR /home/imio
ENV HOME /home/imio
RUN mkdir .buildout && git clone https://github.com/IMIO/${repo}.git
COPY default.cfg .buildout/default.cfg
RUN cd /home/imio/${repo} && ${cmd} && cd /home/imio/ && rm -rf ${repo}
USER root
RUN apt-get clean autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /home/imio/.cache /home/imio/.local
