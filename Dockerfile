FROM docker-staging.imio.be/base:alpine as builder
ENV PIP=9.0.3 \
  ZC_BUILDOUT=2.11.4 \
  SETUPTOOLS=39.1.0 \
  WHEEL=0.31.1 \
  PLONE_MAJOR=4.3 \
  PLONE_VERSION=4.3.18

RUN apk add --update --no-cache --virtual .build-deps \
  build-base \
  gcc \
  git \
  libc-dev \
  libffi-dev \
  libffi-dev \
  libjpeg-turbo-dev \
  libpng-dev \
  libwebp-dev \
  libxml2-dev \
  libxslt-dev \
  openssl-dev \
  pcre-dev \
  wget \
  zlib-dev \
  && pip install pip==$PIP setuptools==$SETUPTOOLS zc.buildout==$ZC_BUILDOUT wheel==$WHEEL
WORKDIR /plone
RUN chown imio:imio -R /plone && mkdir /data && chown imio:imio -R /data
COPY --chown=imio eggs /plone/eggs/
COPY --chown=imio *.cfg /plone/
COPY --chown=imio scripts /plone/scripts
RUN su -c "buildout -c prod.cfg" -s /bin/sh imio


FROM docker-staging.imio.be/base:alpine

ENV PIP=9.0.3 \
  ZC_BUILDOUT=2.11.4 \
  SETUPTOOLS=39.1.0 \
  WHEEL=0.31.1 \
  PLONE_VERSION=4.3.18 \
  TZ=Europe/Brussel

VOLUME /data/blobstorage
VOLUME /data/filestorage
WORKDIR /plone

RUN apk add --no-cache --virtual .run-deps \
  bash \
  rsync \
  libxml2 \
  libxslt \
  libpng \
  libjpeg-turbo

LABEL plone=$PLONE_VERSION \
  os="alpine" \
  os.version="3.10" \
  name="Plone 4.3.18" \
  description="Plone image for iA.Smartweb" \
  maintainer="Imio"

COPY --from=builder /usr/local/lib/python2.7/site-packages /usr/local/lib/python2.7/site-packages
COPY --chown=imio --from=builder /plone .

COPY --chown=imio docker-initialize.py docker-entrypoint.sh /
USER imio
EXPOSE 8081
HEALTHCHECK --interval=1m --timeout=5s --start-period=45s \
  CMD nc -z -w5 127.0.0.1 8081 || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["start"]



ENV ZEO_HOST=db \
 ZEO_PORT=8100 \
 HOSTNAME_HOST=local \
 PROJECT_ID=imio \
 SMTP_QUEUE_DIRECTORY=/data/queue
