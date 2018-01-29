FROM python:rc-alpine

ENV BOARD '  '
ENV TERM ''

RUN apk update
RUN apk add gcc g++ make libffi-dev openssl-dev

RUN pip3 install gspread urllib3 
RUN pip3 install --upgrade beautifulsoup4 oauth2client

RUN mkdir /root/btctalk
ADD board.py /root/btctalk/
ADD Diet-84bfdd7989bd.json /root/btctalk/
RUN chmod a+x /root/btctalk/board.py

CMD python /root/btctalk/board.py $BOARD $TERM


