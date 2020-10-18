"""
work in progress not in use for now.

"""
import pika

class MQ_Service(object):

    def __init__(self,host,port):
        self.host = host
        self.port = port

    def _connect(self,q=None):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host,self.port))
        self.queue=q
        self.channel = connection.channel()
        if self.queue:
            self.channel.queue_declare(queue=self.queue)
        else:
            pass

    def _pub(self,message=None):
        self.channel.basic_publish(exchange = '',
                            routing_key = self.queue,
                            body=message)

    def callback(self,ch, method, properties, body):
            print(" [x] Received %r" % body)

    def _sub(self,callback_func):
        self.channel.basic_consume(callback,
                            queue=self.queue,
                            no_ack=True)

        self.channel.start_consuming()
