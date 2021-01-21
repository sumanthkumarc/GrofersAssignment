FROM python:3.7-stretch
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY /app /app
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["/app/src/app.py"]
