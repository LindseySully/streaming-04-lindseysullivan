# streaming-04-lindseysullivan
### Student Name: Lindsey Sullivan
### Date: 09/13/2023
### Github Repository: https://github.com/LindseySully/streaming-04-lindseysullivan


## Project Prerequisties
1. Git
1. Python 3.7+ (3.11+ Preferred)
1. VS Code Editor
1. VS Code Extension: Python (by Microsoft)
1. VS Code Extension: Docker (by Microsoft)
1. Docker Desktop

## Project Libraries
1. sys
    - Used to provide various functions and variables that can be used to manipulate different parts of the python runtime environment
1. datetime
    - Used to modify the date format of consumer2.py messages
1. time
    - Used to delay the messages sent from producer.py
1. csv
    - Used to read & write to CSV files
1. os
    - Used to specify dedicated paths to directories within the project
1. pika
    - Used to implement the AMQP protocol for RabbitMQ.
1. webbrowser
    - Used to connect to the RabbitMQ Admin webpage

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



# Program Files Overview

## producer.py
The producer program sends information from the spotifytop200songs.csv to dedicated queues. 
- Queue 1: Artist_Information
    - Will send artist_name, artist_num, artist_individual,artist_id from the CSV file
- Queue 2: Song_Information
    - Will send release_date, album_num_tracks, album_cover from the CSV file
- Max_Messages: Set to limit the amount of information streamed, this can be increased or decreased

- offer_rabbitmq_admin_site: offers the user to open the RabbitMQ admin page
- send_to_queue: connect and declare the queue and print message of what queue and server the message was sent to.
    - host (str): host name or IP address of rabbitmq server
    - queue_name (str): the name of the queue
    - message (str): message being sent
- stream_csv_messages: read input file and send each row as a message to a dedicated queue for the worker.
    - input_file_name (str): The name of the CSV file
    - host (str): host name or IP address of the rabbitmq server
    - queue_name (str): the name of the queue
    - messages_sent: counter for messages
    - max_messages: amount of messages to send before closing the connection

## consumer1.py
This consumer program reads messages from the **artist_information** queue. It takes the information and sends the original message to the *original_received_messages.csv*. It also takes the message and transforms the message to all caps, and sends the output to the *artist_message.csv*.

## consumer2.py
This consumer program reads messages from the **song_information** queue. It takes the information and sends the original message to the *original_received_messages.csv*. It also takes the message and transforms the date format from YYYY-MM-DD to DD-MM-YYYY and sends the output to *song_message.csv*.

## /CSV-Files
- Contains all CSV-Files used for the program:
    - Input File: 
        - Spotifytop200songs.csv
    - Output Files:
        - artist_message.csv : messages received from the artist_information queue and the message is now in all caps.
        - song_message.csv : messages received from the song_information queue and the date format is transformed
        - original_received_messages.csv: original messages received from both queues

## Screenshot
![Alt text](<Screenshots/Terminal Output.png>)