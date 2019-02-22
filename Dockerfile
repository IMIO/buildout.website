FROM docker-staging.imio.be/base:latest
MAINTAINER Benoît Suttor <benoit.suttor@imio.be>
ARG repo=buildout.website
RUN mkdir /home/imio/.buildout
ENV PIP=9.0.3 \
  HOME=/home/imio
COPY default.cfg /home/imio/.buildout/default.cfg
RUN buildDeps="python-pip build-essential libpq-dev libreadline-dev wget git gcc libc6-dev libpcre3-dev libssl-dev libxml2-dev libxslt1-dev libbz2-dev libffi-dev libjpeg62-dev libopenjp2-7-dev zlib1g-dev python-dev" \
  && cd /home/imio/ \
  && apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y --no-install-recommends $buildDeps \
  && pip install pip==$PIP \
  && git clone https://github.com/IMIO/${repo}.git ${repo} \
  && cd /home/imio/${repo} \
  && pip install -r requirements.txt \
  && buildout -t 60 -c prod.cfg \
  && cd /home/imio/ \
  && rm -rf ${repo} \
  && chown -R imio:imio /home/imio \
  && apt-get clean autoclean \
  && apt-get purge -y $buildDeps \
  && apt-get autoremove -y \
  && rm -rf /home/imio/.buildout/downloads/ /var/lib/apt/lists/* /tmp/* /var/tmp/* /home/imio/.cache /home/imio/.local
