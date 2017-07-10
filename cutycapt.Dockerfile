FROM ubuntu:16.10

RUN apt-get -qq update
RUN apt-get install -yqq qt4-default xvfb

#xvfb-run --server-args="-screen 0, 1024x768x24" ./CutyCapt --url="http://rozhlas.cz" --out=test.png
