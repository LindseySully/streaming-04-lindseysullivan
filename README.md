# streaming-04-lindseysullivan

## Project Prerequisties
1. Git
1. Python 3.7+ (3.11+ Preferred)
1. VS Code Editor
1. VS Code Extension: Python (by Microsoft)
1. VS Code Extension: Docker (by Microsoft)
1. Docker Desktop

## Docker Setup
#### RabbitMQ Setup
 To run RabbitMQ using a docker container we will complete the following steps. 
1. On the command line run the below command:
    `docker pull rabbitmq`
2. Set up a docker network - this will help with multiple containers needing to communicate with each other. Example: Python Workers & RabbitMQ. Run the following:
    `docker network create mynetwork`
3. Run the RabbitMQ container:
    `docker run -d --name rabbitmq --network mynetwork -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=myuser -e RABBITMQ_DEFAULT_PASS=mypassword`

    - `-- name streaming04rabbig` is the container name for the RabbitMQ container and this names the container
    - `--network mynetwork` connects to the docker network
    - `-p 5672:5672` gives port access to RabbitMQ's advance massage protocol
    - `-p 15672:15672` gives port access to RabbitMQ's web UI port
    - `-e RABBITMQ_DEFAULT_USER=myuser` sets the username for the RabbitMQ Admin Website
    - `-e RABBITMQ_DEFAULT_PASS=mypassword` sets the password for the RabbitMQ Admin Website

#### Producer Setup
To run the python programs in a docker container we will complete the following steps. 
1. Setup the docker-compose.yml to contain items for producer
1. Set up the Dockerfile.producer
    - A DockerFile is necessary in order to eventually create the image which will allow us to run the container. 
1. Run the following in the command line:
    `docker build -t producer-image -f Dockerfile.producer .`
    - This will direct Docker to the correct Dockerfile for the program

#### Consumer Setup
1. Setup the docker-compose.yml to contain items for producer
1. Setup the Dockerfile.consumer
1. Run the following in the command line:
    `docker build -t consumer-image -f Dockerfile.consumer .`

### Troubleshooting Tips:
- Docker may have issues with the docker run code; this can be troubleshooted in the terminal with the following:
    1. Restart Docker:
    `sudo service docker restart`
    1. Check Docker version:
    `docker --version`
    1. Run as root:
    `sudo docker run -d --name streaming04rabbit --network mynetwork -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=myuser -e RABBITMQ_DEFAULT_PASS=mypassword`

- If issues persit then creating the docker-compose.yml file will allow you to run the container using the following command:
    `docker-compose up -d`

- The benefit of this is that it is more maintainable if you plan to add more services to the setup.

## Docker Notes
- Docker can integrate with IDE extensions (which is in the prerequisties). The benefits of this method include:
    - Simpllify Docker Compose for multi-container applications in IDEs
    - Customizable extensions
    - Simplified Debugging of Docker
- Images is what docker creates in-order to run containers
- Create an image by using:
    - `docker build -t <image name> .`
    - the -t flag tags the image with a name
    - . lets docker know where it can find the dockerfile
- Once you run the image in Docker Desktop you can use the link to the localhost to see the admin website for docker

![Alt text](<Screenshots/docker front-in.png>)

### Dockerfile
- This project uses a singular Dockerfile for multiple consumers; the image created from the Dockerfile will run scripts for that will call the consumer programs

# Program File Overview

# Running the Program with Docker
To run the program with Docker we can create a DockerFile to package the program and run it as a container. For this we will do the following:
1. Create a Dockerfile in the same directory as the python program with the following content:
```
FROM python:3.8
# Copy your Python program into the container
COPY your_program.py /app/your_program.py
# Install dependencies
RUN pip install pika
# Run your Python program
CMD ["python", "/app/your_program.py"]
```
1. Replace your_program.py with the program names
1. Build your Docker image and run the container:
```
docker build -t rabbitmq-python-app .
docker run -it --rm --link rabbitmq-container rabbitmq-python-app
```
- This assumes that the RabbitMQ container is running with the name 'rabbit-mq-container'

To run the multiple consumers: use the command
`docker run consumer-image python /app/Consumers/consumer1.py`
`docker run consumer-image python /app/Consumers/consumer2.py`