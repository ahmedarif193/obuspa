import msg_handler
import msg_creator

import stomp
import time

import threading
import logging

conn = stomp.Connection([('localhost', 61613)], heartbeats=(4000, 4000))
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, datefmt="%H:%M:%S")

class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame, body):
        from google.protobuf.message import DecodeError
        for key, value in frame.items() :
            print (key, value)
        msg_handler.MSG_HANDLER_HandleBinaryRecord(body)

    def on_disconnected(self):
        print('disconnected')
#        start_stop(self.conn)




def start_stop(conn):
    conn.set_listener('', MyListener(conn))
    conn.connect('admin1', 'admin1', wait=True)
    #conn.connect('ahmed', 'ahmed', wait=True)
    conn.subscribe(destination='controller', id=101)
    print("conn.connect OK")


def usp_stomp_thread(name):
    start_stop(conn)
    pingRecord = msg_creator.MSG_CREATOR_NewRecord("DM1815209002291", msg_creator.MSG_CREATOR_PING())
    while 1:
        conn.send(body=pingRecord.SerializeToString(), content_type='application/vnd.bbf.usp.msg', destination='agent')
        logging.info("Thread %s: starting", name)
        time.sleep(2)
        logging.info("Thread %s: finishing", name)

def start_server():
    logging.info("Main    : before creating thread")
    x = threading.Thread(target=usp_stomp_thread, args=(1,))
    logging.info("Main    : before running thread")
    x.start()