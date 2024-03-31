FROM python:3.8

RUN mkdir /fastapi_simetra_app

WORKDIR /fastapi_simetra_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x *.sh