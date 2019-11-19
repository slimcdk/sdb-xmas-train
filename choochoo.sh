echo Configuring train

echo Killing existing container
docker stop sdb-train

echo Removing volume
docker  rm sdb-train


echo Building train image
docker build . -t train:latest

echo Starting train image
docker run -tid --restart always --privileged -v /media/usb:/media/usb -v /etc/localtime:/etc/localtime:ro --name=sdb-train train

echo Attatching to container
docker logs --follow sdb-train
