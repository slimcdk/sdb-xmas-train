FROM  balenalib/rpi-raspbian:latest

WORKDIR /app

RUN [ "cross-build-start" ]
RUN install_packages \
    build-essential \
    golang

RUN [ "cross-build-end" ]


ENV UDEV=1

COPY . .

CMD go run .