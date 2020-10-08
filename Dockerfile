FROM imiobe/base:py2-ubuntu-16.04 as builder
MAINTAINER Benoît Suttor <benoit.suttor@imio.be>
ENV PIP=9.0.3 \
  HOME=/home/imio \
  ZC_BUILDOUT=2.11.3 \
  SETUPTOOLS=38.7.0

RUN buildDeps="python-pip build-essential libpq-dev libreadline-dev wget git gcc libc6-dev libpcre3-dev libssl-dev libxml2-dev libxslt1-dev libbz2-dev libffi-dev libjpeg62-dev libopenjp2-7-dev zlib1g-dev python-dev libpq-dev" \
  && apt-get update \
  && apt-get install -y --no-install-recommends $buildDeps \
  && pip install pip==$PIP setuptools==$SETUPTOOLS zc.buildout==$ZC_BUILDOUT \
  && mkdir -p /home/imio/imio-website \
  && chown imio:imio -R /home/imio/imio-website

WORKDIR /home/imio/imio-website
COPY --chown=imio eggs /home/imio/imio-website/eggs/
COPY --chown=imio *.cfg /home/imio/imio-website/
COPY --chown=imio scripts /home/imio/imio-website/scripts
RUN su -c "buildout -c relstorage.cfg -t 30 -N" -s /bin/sh imio

FROM imiobe/base:py2-ubuntu-16.04
ENV PIP=9.0.3 \
  HOME=/home/imio \
  ZC_BUILDOUT=2.11.3 \
  SETUPTOOLS=38.7.0 \
  ZEO_HOST=db \
  ZEO_PORT=8100 \
  HOSTNAME_HOST=local \
  PROJECT_ID=imio

WORKDIR /home/imio/imio-website
COPY --chown=imio --from=builder /home/imio/imio-website .
COPY --from=builder /usr/local/lib/python2.7/site-packages /usr/local/lib/python2.7/site-packages
COPY --from=builder /usr/local/lib/python2.7/dist-packages /usr/local/lib/python2.7/dist-packages
RUN runDeps="poppler-utils wv rsync lynx netcat libxml2 libxslt1.1 libjpeg62 libtiff5 libopenjp2-7 libpq5 git libmagic1" \
  && apt-get update \
  && apt-get install -y --no-install-recommends $runDeps \
  && chown imio:imio /home/imio/imio-website \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER imio
WORKDIR /home/imio/imio-website
