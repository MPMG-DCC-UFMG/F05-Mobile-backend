# F05 Mobile Backend

This project was made using the framework [FastApi](https://fastapi.tiangolo.com/)
and the main goal it's to provide a backend for the developed mobile project.
 
## 1. Setup
 
To run this project first it's necessary to install all dependencies listed in the files
**requirements.txt**. It's advisable that the setup it's made using any kind of 
virtual environment.
 
```bash
pip install -r requirements.txt
```

### 1.1. Environment Variables

This project it's configured to use .env files to set main environment variables. For this project to 
fully work it's necessary to create a **f05_backend.env** file inside the root folder. This file should contain:

```bash
ENVIRONMENT="development"
SENTRY_KEY=<SENTRY_DNS_ADDRESS>
IMAGE_FOLDER="../images/"
```

### 1.2. Docker

It's possible to run the project using docker doing the deployment with docker-compose. 

First it's necessary to build the image. Go to the folder where the **docker-compose.yml** is and
execute:

```bash
docker-compose build
```

After the image it's built the container can be deployed with the command:

```bash
docker-compose up -d
```

To check if the container was successfully deployed open the browser in the 
address ***http://localhost:8000/docs/***

## 2. Documentation

FastAPI offers an automatic documentation of endpoints already implemented using 
Swagger or ReDoc. You can acess this documentation going to:

* Swagger: http://0.0.0.0:8000/docs
* ReDoc: http://0.0.0.0:8000/redoc

## 3. Sponsors

<h1 align="center">
  <a href="https://www.mpmg.mp.br/"><img src="./assets/mmpg_logo.png" alt="MPMG"></a>
  <br>
  <a href="https://sentry.io/"><img src="./assets/sentry-logo-black.png" alt="Sentry"></a>
  <br>
</h1>