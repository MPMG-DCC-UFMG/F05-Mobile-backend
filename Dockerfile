FROM python:3.10

COPY ./ /f05_backend

WORKDIR /f05_backend

RUN pip install -r requirements.txt

RUN mkdir -p ./images

RUN mkdir -p ./reports

WORKDIR /f05_backend/app

RUN pip install -e ./src

CMD python main.py