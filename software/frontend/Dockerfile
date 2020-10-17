FROM  balenalib/rpi-raspbian:latest

WORKDIR /frontend
COPY . .

RUN [ "cross-build-start" ]
RUN install_packages \
    build-essential \
    python3 \
    python3-pip
    
RUN pip3 install --no-cache-dir -r requirements.txt
RUN [ "cross-build-end" ]



#CMD python3 ./conductor.py