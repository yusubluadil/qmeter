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

## Building the Project

Before starting the services, you may need to build or rebuild the Docker images. This is especially important if you have made changes to the Dockerfile or the application code.

### Building Docker Images

To build the Docker images defined in the `docker-compose.yml` file, use the following command:

```bash
docker-compose build

## Starting Services with Docker Compose

To start the services defined in the `docker-compose.yml` file, you use the `docker-compose up` command. This command builds the Docker images (if they do not already exist) and starts the containers.

### Starting Services

To start the services and run them in the foreground, use:

```bash
docker-compose up