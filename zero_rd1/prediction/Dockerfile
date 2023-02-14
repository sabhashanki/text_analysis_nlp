FROM nvidia/cuda:11.3.0-runtime-ubuntu20.04
COPY . /app
WORKDIR /app
RUN set -xe \
    && apt-get update \
    && apt-get -y install python3-pip
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "zero_fastapi:app", "--host=0.0.0.0", "--reload"]
