FROM ubuntu

RUN apt-get -y update && apt-get -y upgrade && apt-get -y install build-essential libssl-dev libdb++-dev libboost-all-dev libcrypto++-dev libqrencode-dev libminiupnpc-dev libgmp-dev libgmp3-dev autoconf autogen automake libtool

RUN git clone https://github.com/TokugawaCoin/Tokugawa.git

RUN cd /Tokugawa/src/ && make -f makefile.unix

RUN cp /Tokugawa/src/Tokugawad /usr/local/bin

RUN mkdir /root/.Tokugawa

ADD Tokugawa.conf /root/.Tokugawa/Tokugawa.conf

CMD Tokugawad 


