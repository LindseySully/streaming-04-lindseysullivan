# streaming-04-lindseysullivan

## Project Prerequisties
1. Git
1. Python 3.7+ (3.11+ Preferred)
1. VS Code Editor
1. VS Code Extension: Python (by Microsoft)
1. VS Code Extension: Docker (by Microsoft)
1. Docker Desktop

## Docker Setup
To run RabbitMQ using a docker container you can put the following in the command line:
    `docker pull rabbitmq`
This will run a RabbitMQ container using the pulled image.
We need to do additional configuration to ensure RabbitMQs admin website and AMQP (Advance Message Protocol) are set up for the ports so we will also run:
    `docker run -d --name rabbitmq-container -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=username -e RABBITMQ_DEFAULT_PASS=password rabbitmq`
    - This will also set a default username and password for the RabbitMQ admin website
    - You may replace the usernmae and password with your desire creditentials

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