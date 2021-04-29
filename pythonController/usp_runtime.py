import msg_handler
import msg_creator

import usp_database

import stomp
import time

import threading
import logging

conn = stomp.Connection([('localhost', 61613)], heartbeats=(4000, 4000))
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, datefmt="%H:%M:%S")

class STOMPListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        from google.protobuf.message import DecodeError
        for key, value in frame.headers.items() :
            print (key, value)
        msg_handler.MSG_HANDLER_HandleBinaryRecord(frame.body)

    def on_disconnected(self):
        print('disconnected')

def start_stop(conn):
    conn.set_listener('', STOMPListener(conn))
    conn.connect('admin1', 'admin1', wait=True)
    #conn.connect('ahmed', 'ahmed', wait=True)
    conn.subscribe(destination='controller', id=101)
    print("conn.connect OK")

def usp_stomp_thread(name):
    usp_database.initdb()
    start_stop(conn)
    devices_registred = usp_database.getRegestredDevices()
    while 1:
        for row in devices_registred:
            pingRecord = msg_creator.MSG_CREATOR_NewRecord(row.device_id, msg_creator.MSG_CREATOR_PING())
            payload_ping_record = pingRecord.SerializeToString()
            conn.send(body=payload_ping_record, content_type='application/vnd.bbf.usp.msg', destination=row.device_topic)
            print ("--------------------------- device_protocol: ",row.device_protocol, "device_topic:",row.device_topic, "device_id:",row.device_id)

        logging.info("Thread %s: starting", name)
        time.sleep(2)

def start_server():

    #conn.send(, 'application/vnd.bbf.usp.msg', 'agent')
    logging.info("Main    : before creating thread")
    x = threading.Thread(target=usp_stomp_thread, args=(1,))
    logging.info("Main    : before running thread")
    x.start()