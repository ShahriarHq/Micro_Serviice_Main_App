# amqps://vzjhuhne:uku10ys-OrFuw9XRb2QFAvjH8ychiyTC@gull.rmq.cloudamqp.com/vzjhuhne
import json

import pika

from main import Product, db, app

params = pika.URLParameters('amqps://vzjhuhne:uku10ys-OrFuw9XRb2QFAvjH8ychiyTC@gull.rmq.cloudamqp.com/vzjhuhne')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main_db')


def callback(ch, method, properties, body):
    print("received in main_db ")
    data = json.loads(body)
    print(data)

    with app.app_context():
        if properties.content_type == 'Product_created':
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('Product created successfully')

        elif properties.content_type == 'Product_updated':
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product updated successfully')

        elif properties.content_type == 'Product_deleted':
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
            print('Product deleted successfully')


channel.basic_consume(queue='main_db', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()
