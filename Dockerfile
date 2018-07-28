FROM python:2.7

RUN apt-get update
RUN pip install CherryPy

ADD . layoutserver
WORKDIR layoutserver

ENTRYPOINT python go.py --layout BAAAHS\ Main.touchosc

EXPOSE 9658/tcp
