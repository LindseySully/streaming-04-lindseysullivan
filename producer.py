"""
   This program emits task from a CSV file and sends the message to a queue on the RabbitMQ server.
   Original source code: Denise Case
   Modifications for CSV input: Lindsey Sullivan
   Date: 09/09/2023

"""

# Import Libraries
import pika
import sys
import webbrowser
import csv
import time
import os

from util_logger import setup_logger
logger, logname = setup_logger(__file__)

# Setup path to directory for CSV file
os.chdir("/Users/lindseysullivan/Documents/School/Streaming-Data/Modules/streaming-04-lindseysullivan/CSV-files")

# Declare Constants
INPUT_CSV_FILE = "spotifytop200songs.csv"
HOST = "localhost"
QUEUE1 = "Artist_Information"
QUEUE2 = "Song_Information"
MAX_MESSAGES = 10 # Define the number of max messages

# ----------------------------------------------------------
# Define Program Functions
# ----------------------------------------------------------
def offer_rabbitmq_admin_site(show_offer):
    """Offer to open the RabbitMQ Admin website"""
    if show_offer == True:
         ans = input("Would you like to monitor RabbitMQ queues? y or n ")
         print()
         if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()
            
def send_to_queue(host: str,queue_name: str,message: str):
    """
    Connect and declare the queue and print message what queue and message was sent. 
    
    Parameters:
        host (str): host name or IP address of rabbitmq server
        queue_name (str): the name of the queue
        message(str): message being sent
    """
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        ch = conn.channel()
        ch.queue_declare(queue=queue_name, durable=True)
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f" [x] Sent to {queue_name}: {message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        conn.close()

def stream_csv_messages (input_file_name: str,host: str,queue_name1: str,queue_name2:str, messages_sent, max_messages):
    """
    Read input CSV file and send each row as a message to a dedicated queue for a dedicated worker.
    
    Parameters:
        input_file_name (str): The name of the CSV file
        host (str): host name or IP address of the rabbitmq server
        queue_name (str): the name of the queue
        messages_sent: counter for messages
        max_messages: amount of messages to send before closing the connection
    """
    try:

        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        ch.queue_declare(queue=queue_name1, durable=True)
        ch.queue_declare(queue=queue_name2, durable=True)

        # initalize messages as empty variables
        message1 = ""
        message2 = ""

        # ensure header row is skipped
        message1 = message1[1:]
        message2 = message2[1:]

        logger.info(f"Reading messages from {input_file_name}...")


        with open(input_file_name,"r",encoding="utf-8") as input_file:
            reader = csv.reader(input_file,delimiter=",")
            next(reader,None) # skip header row
            messages_sent = 0

            for row in reader:
                # join the elements in a row into a single message
                message1 = ",".join([row[index] for index in [4, 5, 6,7]])
                message2 = ",".join([row[index] for index in [11,12,13]])
                # send the message to their respsective queue
                send_to_queue(host,queue_name1,message1)
                send_to_queue(host,queue_name2,message2)
                messages_sent += 1

                # check if the maximum number of messages has been reached
                if messages_sent >= max_messages:
                    logger.info(f"Maximum number of messages ({max_messages}) sent. Closing Connection")
                    break

                time.sleep(3) # wait 3 seconds between messages

        # close the connection after sending the number of messages defined in max_messages
        conn.close()
        logger.info("Connection closed after sending messages.")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    messages_sent = 0
    # ask the user if they'd like to open the RabbitMQ Admin site
    # true shows the offer/false turns off the offer for the user
    offer_rabbitmq_admin_site(show_offer=True)

    # Stream messages from the CSV file and send them to RabbitMQ
    stream_csv_messages(INPUT_CSV_FILE,HOST,QUEUE1,QUEUE2,messages_sent,MAX_MESSAGES)
    
    