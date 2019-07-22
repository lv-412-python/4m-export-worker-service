import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2', port=5672))
channel = connection.channel()

channel.queue_declare(queue='export')

channel.basic_publish(exchange='', routing_key='export', body="{'task_id': 100000000, 'form_id': 1, 'groups': [], 'export_format': 'xls', 'email': 'leorik09@gmail.com'}")
print(" [x] Sent 'Hello World!'")
connection.close()

print('111111111111111111111111111')