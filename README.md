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

It's also necessary to install the current application as a library in your python installation.
Go to the folder **/app/src** and run the command:

```bash
pip install -e .
```

### 1.1. Environment Variables

This project it's configured to use .env files to set main environment variables. For this project to 
fully work it's necessary to create a **f05_backend.env** file inside the root folder. This file should contain:

```bash
ENVIRONMENT="development"
SENTRY_KEY=<SENTRY_DNS_ADDRESS>
IMAGE_FOLDER="../images/"
DATABASE_URL="sqlite:///./sql_app.db"
API_PREFIX="" 
TOKEN_CEP_ABERTO=<TOKEN_CEP_ABERTO>
SECRET_KEY=<SECRET_KEY_TO_GENERATE_TOKEN>
API_KEY=<GENERATED_API_KEY>
```

#### 1.1.1 Secret Key

To generate a secret key string that's valid for this project run in the command line:

```bash
openssl rand -hex 32
```

Copy the result and past as a string in the environment file.

### 1.1.2 API Key

To improve app security it's used an API key to wrap all calls. Can be passed as a header
or a query parameter with the name **X-TRENA-KEY**.

In order to fill this API Key a strong password generator with 20 digits result can be used.

### 1.2. Database

The project it's configured to use SQLAlchemy as framework to make the connection with database. For the development of this 
project was used **SQLite** database, and the deployment made with PostgreSQL using docker-compose configuration.

The environment variable **DATABASE_URL** on the file created in section 1.1 it's used to tell the service to what database connect.
If used the same configuration as exemplified previously **SQLite** will be used.

#### 1.2.1. PostgreSQL

Docker-compose will be used to deploy PostgreSQL and pgAdmin4 into host.

First step it's to create a file called **database.env** in the same folder as the file **docker-compose.yml**. The content of the file
will be:

```bash
# database.env
POSTGRES_USER=mp_user
POSTGRES_PASSWORD=magical_password_example
POSTGRES_DB=mp_f05_database
```

Now create the docker-compose with the following lines making the necessary changes into password and email:

```bash
services:

  database:
      image: postgres
      env_file:
        - database.env # configure postgres
      ports:
        - "15432:5432"
      volumes:
        - database-data:/var/lib/postgresql/data/ # persist data even if container shuts down
      networks:
        - postgres-compose-network

  pgAdmin:
        image: dpage/pgadmin4
        environment:
          PGADMIN_DEFAULT_EMAIL: <EMAIL>
          PGADMIN_DEFAULT_PASSWORD: <PG_PASSWORD>
        ports:
          - "16543:80"
        depends_on:
          - database
        networks:
          - postgres-compose-network

volumes:
    database-data: # named volumes can be managed easier using docker-compose

networks: 
    postgres-compose-network:
        driver: bridge
```

After everything it's set, go to the file **f05_backend_env** and change the **DATABASE_URL** value.

Using the values of this example we will have:

````bash
DATABASE_URL = "postgresql://mp_user:magical_password_example@mp_f05_database/db"
````

With this we have a connection onto the database

All files of this project can be used as an example of how your production environment files should
look like.

### 1.3. Docker

It's possible to run the project using docker doing the deployment with docker-compose, building locally or
getting the docker image from github package repository.

To build the image locally from source code run: 

```bash
docker build -t f05_backend . 
```

Add the following lines to your compose that has database values:

```bash
    f05_backend:
        #Uncoment the two following lines and comment image if you want to build from local project
        #build: ./ 
        #container_name: "f05_backend"
        image: docker.pkg.github.com/mpmg-dcc-ufmg/f05-mobile-backend/f05-backend-image:v1.1.2
        labels:
          - "traefik.http.routers.f05_backend.rule=PathPrefix(`/f05_backend`)"
          - "traefik.http.services.f05_backend.loadbalancer.server.port=8000"
          - "traefik.http.middlewares.f05_backend.stripprefix.prefixes=/f05_backend"
          - "traefik.http.routers.f05_backend.middlewares=f05_backend@docker"
        volumes:
          - ./images/:/f05_backend/images
          - ./f05_backend_prod.env:/f05_backend/f05_backend.env
        depends_on:
          - database
        networks:
          - postgres-compose-network
          - internal
```

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
address ***http://localhost/f05_backend/docs/***

If it's necessary to enter the shell to run alembic migrations or run scripts execute:

```bash
docker-compose exec f05_backend sh 
```

Container's logs can be seen using:

```bash
docker-compose logs f05_backend
```

### 1.4 Third Party

Some third party solutions are used to deliver features: 

* [CEP Aberto](https://cepaberto.com/) : It is a project that aims to provide free access and collaboratively 
build a database with the geolocalized Postal Address Codes (CEP) from all over Brazil. **It's necessary to
get an API Key from this service in order to use the get address by CEP feature**

### 1.3.1 Useful commands

1. Prune unused docker images, volumes and containers:

```bash
docker system prune -a
```

2. Remove all images 

```bash
docker rmi $(docker images -a -q)
```

3. Stop and remove all containers

```bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

4. Remove all volumes

```bash
docker volume prune
```

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