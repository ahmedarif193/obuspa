import os
import time
import stomp
import usp_record_1_1_pb2
import usp_msg_1_1_pb2
from pprint import pprint
from google.protobuf import text_format
import msg_handler

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

class USP_MsgType:
    GET = 1;
    GET_RESP = 2;
    NOTIFY = 3;
    SET = 4;
    SET_RESP = 5;
    OPERATE = 6;
    OPERATE_RESP = 7;
    ADD = 8;
    ADD_RESP = 9;
    DELETE = 10;
    DELETE_RESP = 11;
    GET_SUPPORTED_DM = 12;
    GET_SUPPORTED_DM_RESP = 13;
    GET_INSTANCES = 14;
    GET_INSTANCES_RESP = 15;
    NOTIFY_RESP = 16;
    GET_SUPPORTED_PROTO = 17;
    GET_SUPPORTED_PROTO_RESP = 18;



record = usp_record_1_1_pb2.Record()
#msg.header
msg = usp_msg_1_1_pb2.Msg()
msg.header.msg_type = USP_MsgType.GET_SUPPORTED_DM
msg.header.msg_id = "101"
msg.body.request.get_supported_dm.obj_paths.extend(["Device."])
msg.body.request.get_supported_dm.first_level_only = 0
msg.body.request.get_supported_dm.return_commands = 0
msg.body.request.get_supported_dm.return_events = 0
msg.body.request.get_supported_dm.return_params = 1

record.from_id = "test1"
record.to_id = "test2"
record.version = "1.0"
record.payload_security = 0
record.no_session_context.payload = msg.SerializeToString()

print(text_format.MessageToString(record))
print(text_format.MessageToString(msg))

conn.set_listener('', MyListener(conn))
connect_and_subscribe(conn)
time.sleep(60)
conn.disconnect()