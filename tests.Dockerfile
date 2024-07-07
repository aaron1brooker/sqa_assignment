FROM python:3.10-alpine3.14
WORKDIR /src
RUN pip install --upgrade pip
COPY ./ ./
RUN pip install -r ./requirements-dev.txt
ENV FLASK_APP=app
CMD ["python3", "-m", "pytest", "tests/integration/tests.py"]