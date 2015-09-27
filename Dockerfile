FROM alpine:3.2
MAINTAINER Eran Zimbler <eran@zimbler.net>


RUN apk --update add python libxml2-dev libxslt-dev
RUN apk --update add --virtual build-dependencies py-pip python-dev build-base  && pip install virtualenv
  


WORKDIR /src
COPY . /src

RUN ln -s /usr/include/libxml2/libxml /usr/include/libxml
RUN virtualenv env && env/bin/pip install -r ./requirements.txt
RUN apk del build-dependencies && rm -rf /var/cache/apk/*

CMD ["env/bin/python", "add_to_lib.py"]