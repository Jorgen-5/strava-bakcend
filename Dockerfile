
FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3.9 

RUN apt-get update && apt-get install -y  \
    python3-pip

ADD requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt



ADD . /app/
WORKDIR /app/
ENV PYTHONPATH=/app/

CMD ["python3", "-u", "app/app.py"]



