FROM  balenalib/rpi-raspbian:latest

ENV UDEV=1


WORKDIR /app
COPY . .


RUN [ "cross-build-start" ]
RUN install_packages \
    build-essential \
    git \
    wget \
    golang \
    omxplayer

RUN go mod download
#RUN go test
RUN go build

RUN [ "cross-build-end" ]

CMD ./sdb-xmas-train