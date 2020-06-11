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
DATABASE_URL="sqlite:///./sql_app.db"
```

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