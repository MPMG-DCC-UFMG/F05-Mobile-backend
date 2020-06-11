FROM python:3.7

COPY ./ /f05_backend

WORKDIR /f05_backend

RUN pip install -r requirements.txt

RUN mkdir -p ./images

WORKDIR /f05_backend/app

CMD python main.py