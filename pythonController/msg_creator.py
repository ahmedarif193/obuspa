import usp_commons
import random

def MSG_CREATOR_NewRecord(to_id, usp_msg):
    record = usp_commons.usp_record_1_1_pb2.Record()
    record.from_id = "controller1"
    record.to_id = to_id
    record.version = "1.0"
    record.payload_security = 0
    record.no_session_context.payload = usp_msg.SerializeToString()
    return record

def MSG_CREATOR_REQUEST_GET(requestedpath):
    msg = usp_commons.usp_msg_1_1_pb2.Msg()
    msg.header.msg_type = usp_commons.USP_MsgType.GET
    uniqueID = random.randint(10, 6000)
    msg.header.msg_id = str(uniqueID)
    msg.body.request.get.param_paths.extend([requestedpath])
    return msg

def MSG_CREATOR_REQUEST_SET(requestedpath,param,value):
    msg = usp_commons.usp_msg_1_1_pb2.Msg()
    msg.header.msg_type = usp_commons.USP_MsgType.GET
    uniqueID = random.randint(10, 6000)
    msg.header.msg_id = str(uniqueID)
    param_obj1 = msg.body.request.set.update_objs.add()
    param_obj1.obj_path= requestedpath
    param_obj1.param_settings.add(param=param, value=value)
    return msg

def MSG_CREATOR_PING():
    msg = usp_commons.usp_msg_1_1_pb2.Msg()
    msg.header.msg_type = usp_commons.USP_MsgType.GET
    uniqueID = random.randint(10, 6000)
    msg.header.msg_id = str(uniqueID)
    msg.body.request.get.param_paths.extend(["Device.LocalAgent.UpTime"])
    return msg