FROM ubuntu:16.10

RUN apt-get -qq update
RUN apt-get install -yqq build-essential subversion qt4-default
RUN mkdir -p /build/cutycapt
WORKDIR /build/cutycapt
RUN svn checkout svn://svn.code.sf.net/p/cutycapt/code/ cutycapt-code
WORKDIR /build/cutycapt/cutycapt-code/CutyCapt

RUN apt-get install -yqq libqtwebkit-dev

# TODO put into /build/cutycapt/cutycapt-code/CutyCapt/CutyCapt.hpp
RUN echo "#include <QNetworkReply>" | tee -a /build/cutycapt/cutycapt-code/CutyCapt/CutyCapt.hpp
RUN echo "#include <QSslError>" | tee -a /build/cutycapt/cutycapt-code/CutyCapt/CutyCapt.hpp
##include <QSslError>


RUN qmake
RUN make

#TODO remove later
#RUN apt-get install -yqq libqt4webkit5-dev
#RUN apt-get install -yqq libqt4svg*
#RUN apt-get install -yqq libqt4-webkit libqt4-dev g++
