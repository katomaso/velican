FROM python:3

RUN apt update && \
    apt install -y git

COPY requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt

VOLUME /app

EXPOSE 8080

ENV FLASK_APP="velican"

ENTRYPOINT ["/bin/bash"]