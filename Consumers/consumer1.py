"""
    This program listens for work messages contiously. 
    It looks for the messages and sends the messages to the CSV output file.
    Start multiple versions to add more workers.  
    Original source code by Denise Case
    Modifications to code for CSV file: Lindsey Sullivan - 9/10/23

"""

import pika
import sys
import time
import csv
import os

# define queue
QUEUE = "Artist_Information"

# define the relative path for the CSV files
csv_files_directory = "../CSV-Files"

# define output CSV files
OUTPUT_CSV_FILE1 = os.path.join(csv_files_directory,"original_received_messages.csv")
OUTPUT_CSV_FILE2 = os.path.join(csv_files_directory,"artist_message.csv")

# define a callback function to be called when a message is received
def callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # decode the binary message body to a string
    message = body.decode()

    #transform message to all upper case
    transformed_message = message.upper()

    print(f" [x] Received {message}")
    # simulate work by sleeping for the number of dots in the message
    time.sleep(len(message))
    # Log message before writing to the CSV file
    print(f" [x] Writing message to CSV: {message}")

    # write the original message to csv file
    with open(OUTPUT_CSV_FILE1,"a",newline="")as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([message])
    
    # write the transformed columns to a new csv
    with open(OUTPUT_CSV_FILE2,"a",newline="")as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([transformed_message])


    # Log message after writing to the original received CSV file
    print(f" [x] Message written to original message CSV: {message}")
    # Log message after writng to the new CSV file
    print(f" [x] Message written to Artist CSV {transformed_message}")
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# define a main function to run the program
def main(hn: str, input_queue: str,output_csv_file1,output_csv_file2):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=input_queue, durable=True)

        # The QoS level controls the # of messages
        # that can be in-flight (unacknowledged by the consumer)
        # at any given time.
        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed
        # and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # open the original messages CSV output file for writing
        csv_file = open(output_csv_file1, "w",newline="")
        csv_writer = csv.writer(csv_file)

        # open the artist csv output for writing
        csv_file = open(output_csv_file2,"w",newline="")
        csv_writer = csv.writer(csv_file)

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume(queue=input_queue, on_message_callback=callback, auto_ack=False)

        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main("localhost",QUEUE,OUTPUT_CSV_FILE1,OUTPUT_CSV_FILE2)
