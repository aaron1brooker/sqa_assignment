FROM python:3.10-alpine3.14
WORKDIR /src
RUN apk update && \
    apk add curl
RUN pip install --upgrade pip
COPY . /src
RUN pip install -r /src/requirements.txt
ENV FLASK_APP=app
CMD ["python3","main.py"]