import usp_record_1_1_pb2
import usp_msg_1_1_pb2
from pprint import pprint
from google.protobuf import text_format
from google.protobuf.message import DecodeError
import json
from dict_shortcuts import *

def MSG_SENGER_GetRequest(msg_id,src,dest,path):
    record = usp_record_1_1_pb2.Record()
    msg = usp_msg_1_1_pb2.Msg()
    msg.header.msg_id = msg_id
    msg.header.msg_type = 1 #GET
    msg.body.request.get.param_paths.append(path) 
    record.no_session_context.payload = msg.SerializeToString()
    record.version = '1.0'
    record.to_id = dest
    record.from_id = src
    record.payload_security = 0
    print(msg)
    print(record)

def MSG_HANDLER_HandleBinaryRecord(stomp_msg):
    print('----- >>>> MSG_HANDLER_HandleBinaryRecord',stomp_msg)
    record = usp_record_1_1_pb2.Record()
    try:
        record.ParseFromString(str.encode(stomp_msg))
    except DecodeError:
        print('----- >>>> DecodeError',DecodeError)
    else:
        agent_endpoint = record.from_id
        MSG_HANDLER_HandleBinaryMessage(record.no_session_context.payload,agent_endpoint)

def MSG_HANDLER_HandleBinaryMessage(record_payload,agent_endpoint):
    msg = usp_msg_1_1_pb2.Msg()
    try:
        msg.ParseFromString(record_payload)
    except DecodeError:
        print('----- >>>> MSG_HANDLER_HandleBinaryMessage>>>>>>>>>>>> DecodeError')
    HandleUspMessage(msg,agent_endpoint)

#at this state we can reply ---------------------------------------
def HandleUspMessage(usp_msg,agent_endpoint):
    #handle usp_msg.body.error
    if usp_msg.header.msg_type == 2 :
        MSG_HANDLER_HandleGet_resp(usp.header.msg_id,usp_msg.body.response,agent_endpoint)

def MSG_HANDLER_HandleGet_resp(msg_id,response_payload,agent_endpoint):
    #print('----- >>>> MSG_HANDLER_HandleGet',response_payload)
    #print('----- >>>> record_payload.body.response.get_resp.req_path_results',response_payload.get_resp)
    i = 0
    count_get = len(response_payload.get_resp.req_path_results)
    while i < count_get:
        MSG_HANDLER_HandleGet_RequestedPathResult(msg_id,response_payload.get_resp.req_path_results[i],agent_endpoint)
        i += 1

def MSG_HANDLER_HandleGet_RequestedPathResult(msg_id,RequestedPathResult_payload,agent_endpoint):
    print(RequestedPathResult_payload)
    print(agent_endpoint)
    #TODO : HANDLE ERRORs :
    #string requested_path = 1;
    #fixed32 err_code = 2;
    #string err_msg = 3;
    count_get = len(RequestedPathResult_payload.resolved_path_results)
    i = 0
    while i < count_get:
        MSG_HANDLER_HandleGet_ResolvedPathResult(msg_id,RequestedPathResult_payload.resolved_path_results[i],agent_endpoint)
        i += 1

def MSG_HANDLER_HandleGet_ResolvedPathResult(ResolvedPathResult_payload,agent_endpoint):
    count_get = len(ResolvedPathResult_payload.result_params)
    for key, value in ResolvedPathResult_payload.result_params.items():
        MSG_HANDLER_HandleGet_resp_Value(msg_id,agent_endpoint, ResolvedPathResult_payload.resolved_path, key, value)

def MSG_HANDLER_HandleGet_resp_Value(msg_id,agent_endpoint,path_entry,key,value):
    print('----->>>> MSG_HANDLER_HandleGet_resp_Value : ',msg_id, agent_endpoint, path_entry, key, value)