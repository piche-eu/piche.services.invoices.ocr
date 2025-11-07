import pika

credentials = pika.PlainCredentials('kakadu', '1dc20fba-c298-402c-9c73-483753b4102a')
parameters = pika.ConnectionParameters('rabbit-tcp.gpark.lv',
                                   443,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                  routing_key='hello',
                  body='Hello W0rld!')

print(" [x] Sent 'Hello World!'")
connection.close()