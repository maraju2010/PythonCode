import pika
import time
import threading
import logging

class MQService(object):
    def __init__(self,logger):
        try:
            self.logging = logger
            self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost",5672,heartbeat_interval=600))
            logging.info(self.connection)
            self.flag = 0
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='UCMONQUEUE')
            #self.channel.queue_declare(queue='UCREGQUEUE')
            try:
                t2 = threading.Thread(target=self.Thread_HB)
                t2.setDaemon(True)
                t2.start()
            except Exception as e:
                self.logging.info(e)
            self.logging.info("webserver mq on")
        except Exception as e:
                self.logging.info(e)

    def _run(self,message):
        try:
            self.flag=1
            ignore1,Queue= message.partition(',')[0].split("=",1)
            ignore2,msg= message.split(",",1)
            self.logging.info("mq webserver %s" % msg)
            if Queue=="UCREGQUEUE":
                self.channel.basic_publish(exchange='',
                                routing_key='UCREGQUEUE',
                                body=msg,
                                mandatory=True)
                self.flag=0
            else:
                self.channel.basic_publish(exchange='',
                                routing_key='UCMONQUEUE',
                                body=msg,
                                mandatory=True)
                self.flag=0
        except Exception as e:
            self.logging.info(e)

    def Thread_HB(self):
        while(True):
            self.connection.process_data_events()
            time.sleep(30)
        #self.connection.sleep(30)

    #def receive(self):
    #    '''rabbitmq receiver'''
    #$    print("rabbitmq hearbeat thread on\n")
    #    self.cb()
    #    self.channel.basic_consume(self.cb,'UCMONQUEUE')
    #    self.channel.start_consuming()

    #def cb(self,ch,method,properties,body):
    #def cb(self):
    #    print("heart beating")
        #self.Thread_HB()
        #time.sleep(30)

    def _close(self):
        self.connection.close()
