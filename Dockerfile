FROM docker-staging.imio.be/base:latest

RUN apt-get -qy update && apt-get -qy install gcc python27 python27-virtualenv python27-setuptools libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev
RUN mkdir /home/imio/website
COPY . /home/imio/website
RUN chown imio:imio -R /home/imio/website
USER imio
WORKDIR /home/imio/website
RUN /opt/python2.7.8/bin/python bootstrap.py
RUN bin/buildout -t 7 -c docker.cfg
USER root
RUN apt-get remove -y gcc libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev
RUN apt-get autoremove -y
USER imio
ENV HOME /home/imio/website
ENV ZEO_HOST db
ENV ZEO_PORT 8100
ENV HOSTNAME_HOST local
ENV PROJECT_ID imio

CMD /home/imio/website/bin/zeoserver fg
EXPOSE 8080

VOLUME ["/home/imio/website/var/blobstorage", "/home/imio/website/var/filestorage"]
