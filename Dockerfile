FROM docker-staging.imio.be/base:latest
RUN mkdir /home/imio/imio-website
COPY *.cfg /home/imio/imio-website/
COPY Makefile /home/imio/imio-website/
COPY *.py /home/imio/imio-website/
RUN chown 913:209 -R /home/imio/imio-website/
WORKDIR /home/imio/imio-website
RUN \
    apt-get -qy update && apt-get -qy install gcc python27 python27-virtualenv python27-setuptools libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev &&\
    sudo -u imio bash -c '/opt/python2.7.8/bin/python bootstrap.py' &&\
    sudo -u imio bash -c 'make buildout-docker' &&\
    apt-get remove -y gcc gcc-4.8 cpp-4.8 zsh-common libruby1.9.1 &&\
    apt-get autoremove -y &&\
    apt-get clean
USER imio
ENV HOME /home/imio/imio-website
ENV ZEO_HOST db
ENV ZEO_PORT 8100
ENV HOSTNAME_HOST local
ENV PROJECT_ID imio