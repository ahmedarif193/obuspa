import os
import time
import stomp
import usp_record_1_1_pb2
import usp_msg_1_1_pb2
from pprint import pprint
from google.protobuf import text_format
import msg_handler

msg_handler.MSG_SENGER_GetRequest('1025','controller','agent','Device.STOMP.Connection.1.Alias')
conn = stomp.Connection([('localhost', 61613)], heartbeats=(4000, 4000))

def connect_and_subscribe(conn):
    conn.connect('admin1', 'admin1', wait=True)
    conn.subscribe(destination='controller', id=101)
    print("conn.connect OK")

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
        connect_and_subscribe(self.conn)

record = usp_record_1_1_pb2.Record()
#msg.header
record.from_id = "test1"
record.to_id = "test2"
conn.set_listener('', MyListener(conn))
connect_and_subscribe(conn)
time.sleep(60)
conn.disconnect()