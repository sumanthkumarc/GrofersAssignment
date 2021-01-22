FROM python:3.7-stretch
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY /src /src
WORKDIR /src
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:/src
ENTRYPOINT ["python"]
CMD ["/src/run.py"]
