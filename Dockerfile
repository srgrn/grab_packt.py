FROM gliderlabs/alpine:3.2

RUN apk update
RUN apk add \
    python \
    python-dev \
    py-pip \
    build-base \
    libxml2-dev \
    libxslt-dev \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

WORKDIR /src
COPY . /src

RUN ln -s /usr/include/libxml2/libxml /usr/include/libxml
RUN virtualenv env && env/bin/pip install -r ./requirements.txt

CMD ["env/bin/python", "add_to_lib.py"]