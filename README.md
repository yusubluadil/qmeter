# QMeter Project

This repository contains a Django project integrated with MongoDB, using Docker for containerization. This README provides instructions on setting up and running the project.

## Requirements

- Python 3.8 or higher
- Docker
- Docker Compose

## Setup

1. **Environment Variables**

   Create a `.env` file in the root directory of the project with the following content:

   ```env
   #== Django ==#
   DJANGO_SECRET_KEY=example_django_secret_key
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

   #== Mongo DB ==#
   MONGO_DB_NAME=qmeterDB
   MONGO_DB_URI=mongodb://mongo:27018/qmeterDB

## Building and Starting Services with Docker Compose

To build the Docker images and start the services defined in the `docker-compose.yml` file, you can use the `docker-compose up` command with the `--build` option. This ensures that the images are rebuilt with the latest changes before starting the containers.

### Build and Start Services

To build the Docker images (if they do not already exist) and start the containers, use:

```bash
docker-compose up --build