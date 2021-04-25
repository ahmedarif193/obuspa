import usp_commons

import os
import time
import stomp
import usp_record_1_1_pb2
import usp_msg_1_1_pb2
from pprint import pprint
from google.protobuf import text_format
import msg_handler
import msg_creator
import usp_runtime


#---------------------------
# MSG TYPE HANDLER 
#---------------------------



msg1 = msg_creator.MSG_CREATOR_REQUEST_GET("Device.BulkData.")
record1 = msg_creator.MSG_CREATOR_NewRecord("DM1815209002291", msg1)
msg = usp_msg_1_1_pb2.Msg()

usp_runtime.start_server()
#usp_runtime.conn.send(body=record1.SerializeToString(), content_type='application/vnd.bbf.usp.msg', destination='agent')
time.sleep(60)
#conn.disconnect()