echo Configuring normalizer

echo Killing existing container
docker stop normalizer

echo Removing volume
docker rm normalizer

echo Building normalizer image
docker build . -t normalizer:latest

echo Starting normalizer image
docker run -v /media/usb:/media/usb --name=normalizer normalizer

echo Attatching to container
docker logs --follow normalizer
