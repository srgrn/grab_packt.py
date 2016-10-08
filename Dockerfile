FROM alpine:3.4
MAINTAINER Eran Zimbler <eran@zimbler.net>

WORKDIR /src
COPY . /src

RUN apk --update add libxml2-dev libxslt-dev && \ 
    apk --update add --virtual build-dependencies python3 python3-dev build-base && \
    ln -s /usr/include/libxml2/libxml /usr/include/libxml && \
    python3 -m ensurepip && pip3 install --upgrade pip && \
    pip install -r ./requirements.txt && \
    apk del build-dependencies && rm -rf /var/cache/apk/*

CMD ["env/bin/python", "add_to_lib.py"]