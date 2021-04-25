import usp_record_1_1_pb2
import usp_msg_1_1_pb2
import time

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
