FROM docker-staging.imio.be/iasmartweb/cache:latest
RUN mkdir /home/imio/imio-website
COPY *.cfg /home/imio/imio-website/
COPY Makefile /home/imio/imio-website/
COPY *.py /home/imio/imio-website/
COPY scripts /home/imio/imio-website/scripts
RUN chown imio:imio -R /home/imio/imio-website/
WORKDIR /home/imio/imio-website
USER imio
RUN /usr/bin/python bootstrap.py -c prod.cfg &&\
    make buildout-prod
USER root
RUN apt-get remove -y gcc python-dev &&\
    apt-get autoremove -y &&\
    apt-get clean
USER imio
ENV ZEO_HOST db
ENV ZEO_PORT 8100
ENV HOSTNAME_HOST local
ENV PROJECT_ID imio
