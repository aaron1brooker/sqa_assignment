# FROM python:3.10

# RUN pip install mysql-connector-python

# WORKDIR /usr/app/src

# COPY db_interactions.py ./

FROM python:3.9.10-alpine3.14
WORKDIR /src
RUN pip install --upgrade pip
RUN pip install flask
COPY . /src
ENV FLASK_APP=app
CMD ["python3","main.py"]