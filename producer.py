# # amqps://vzjhuhne:uku10ys-OrFuw9XRb2QFAvjH8ychiyTC@gull.rmq.cloudamqp.com/vzjhuhne
import pika
import json
import time

params = pika.URLParameters('amqps://vzjhuhne:uku10ys-OrFuw9XRb2QFAvjH8ychiyTC@gull.rmq.cloudamqp.com/vzjhuhne')


def connect():
    return pika.BlockingConnection(params)


def publish(method, body):
    properties = pika.BasicProperties(method)
    connection = connect()
    channel = connection.channel()

    for attempt in range(3):  # Try up to 3 times
        print("Retrying for " + str(attempt) + " times")
        try:
            channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
            break
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection error: {e}, retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            connection = connect()
            channel = connection.channel()
        except pika.exceptions.StreamLostError as e:
            print(f"Stream lost error: {e}, retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            connection = connect()
            channel = connection.channel()
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    else:
        print("Failed to publish message after 3 attempts")

    # Ensure the connection is closed after use
    if connection.is_open:
        connection.close()
