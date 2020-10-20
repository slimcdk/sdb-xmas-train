FROM  balenalib/rpi-raspbian:latest

ENV UDEV=1


WORKDIR /app
COPY . .
#COPY ../../go.mod .
#COPY ../../go.sum .


RUN [ "cross-build-start" ]
RUN install_packages \
    build-essential \
    git \
    wget \
    golang \
    omxplayer

#RUN go mod download
#RUN go test
RUN go build

RUN [ "cross-build-end" ]

CMD ./conductor