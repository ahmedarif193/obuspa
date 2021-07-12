#!/bin/python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy_serializer import SerializerMixin

engine = create_engine("mysql+pymysql://uspuser:uspuser@localhost/USP_DATABASE?charset=utf8mb4")

Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()

class Devices(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key = True)
    device_ip_addr = Column(String(255))
    device_protocol = Column(String(255))
    device_topic = Column(String(255))
    device_id = Column(String(255))

class LogMessages(Base, SerializerMixin):
    __tablename__ = 'log_messages'
    id = Column(Integer, primary_key = True)
    log_from = Column(String(255))
    log_to = Column(String(255))
    log_type = Column(Integer)
    log_date = Column(DateTime, default=datetime.datetime.utcnow)

def initdb():
    Base.metadata.create_all(engine)

initdb()

def getSession():
    return session

def getRegestredDevices():
    return session.query(Devices).all()
    
def deleteDevice(deviceId):
    session.query(Devices).filter(Devices.id==deviceId).\
        delete(synchronize_session=False)
    session.commit()

def addDevice(device_ip_addr,device_protocol,device_topic,device_id):
    device = Devices(device_ip_addr = device_ip_addr, device_protocol = device_protocol, device_topic = device_topic, device_id = device_id)
    session.add(device)
    session.commit()

def Sql_Log(log_from, log_to, log_type):
    entry = LogMessages(log_from = log_from, log_to = log_to, log_type = log_type)
    session.add(entry)
    session.commit()

#device1 = Devices(device_ip_addr = '172.0.0.1', device_protocol = 'STOMP', device_topic = 'agent', device_id = 'DM1815209002291')
#session.add(device1)
#session.commit()

devices_registred = session.query(Devices).all()

for row in devices_registred:
       print ("device_protocol: ",row.device_protocol, "device_topic:",row.device_topic, "device_id:", row.device_id)
