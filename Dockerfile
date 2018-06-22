FROM docker-staging.imio.be/base:latest
MAINTAINER Benoît Suttor <benoit.suttor@imio.be>
ARG repo=buildout.website
RUN buildDeps="python-pip build-essential libpq-dev libreadline-dev wget git gcc libc6-dev libpcre3-dev libssl-dev libxml2-dev libxslt1-dev libbz2-dev libffi-dev libjpeg62-dev libopenjp2-7-dev zlib1g-dev python-dev" \
  && apt-get update \
  && apt-get install -y --no-install-recommends $buildDeps \
  && pip install -U pip
USER imio
WORKDIR /home/imio
ENV HOME /home/imio
RUN mkdir .buildout && git clone https://github.com/IMIO/${repo}.git ${repo}
COPY default.cfg .buildout/default.cfg
WORKDIR /home/imio/${repo}
USER root
RUN pip install -r requirements.txt
USER imio
RUN buildout -c prod.cfg
WORKDIR /home/imio/
RUN rm -rf ${repo}
USER root
RUN apt-get clean autoclean \
  && apt-get purge -y $buildDeps \
  && apt-get autoremove -y \
  && rm -rf /home/imio/.buildout/downloads/ /var/lib/apt/lists/* /tmp/* /var/tmp/* /home/imio/.cache /home/imio/.local
