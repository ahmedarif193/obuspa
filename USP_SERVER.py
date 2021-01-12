import os
import time
import stomp
import usp_record_1_1_pb2
import usp_msg_1_1_pb2
from pprint import pprint
from google.protobuf import text_format

def connect_and_subscribe(conn):
    conn.connect('admin1', 'admin1', wait=True)
    conn.subscribe(destination='agent', id=123)
    print("conn.connect OK")

class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame, param3):
        from google.protobuf.message import DecodeError
        for key, value in frame.items() :
            print (key, value)
        record = usp_record_1_1_pb2.Record()
        try:
            record.ParseFromString(str.encode(param3))
        except DecodeError:
            print('----- >>>> DecodeError')
#        print('---------------------->>>>>>>>>',record.from_id)
#        print('---------------------->>>>>>>>>',record.to_id)
        print('---------------------->>>>>>>>>',text_format.MessageToString(record))
        msg = usp_msg_1_1_pb2.Msg()
        try:
            msg.ParseFromString(record.no_session_context.payload)
        except DecodeError:
            print('----- >>>> DecodeError  msg.ParseFromString(str.encode(record.no_session_context.payload))')
        print('---------------------->>>>>>>>>',text_format.MessageToString(msg))
 #       print('---------------------->>>>>>>>>',text_format.MessageToString(msg))
    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)
record = usp_record_1_1_pb2.Record()
#msg.header
record.from_id = "test1"
record.to_id = "test2"

print("TESTTTTTT")
conn = stomp.Connection([('localhost', 61613)], heartbeats=(4000, 4000))
print("TESTTTTTT2")

conn.set_listener('', MyListener(conn))
print("TESTTTTTT23")

connect_and_subscribe(conn)
print("TESTTTTTT4")

time.sleep(60)
print("TESTTTTTT5")

conn.disconnect()