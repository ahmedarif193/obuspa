#!venv/bin/python
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///usp_gui.db', echo = True)
Base = declarative_base()
Session = sessionmaker(bind = engine)

class Devices(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key = True)
    device_ip_addr = Column(String)
    device_protocol = Column(String)
    device_topic = Column(String)
    device_id = Column(String)

def initdb():
    Base.metadata.create_all(engine)

initdb()

#device1 = Devices(device_ip_addr = '172.0.0.1', device_protocol = 'STOMP', device_topic = 'agent', device_id = 'DM1815209002291')
#session.add(device1)
#session.commit()


result = session.query(Devices)


for row in result:
       print ("ID:", row.id, "Name: ",row.device_protocol, "Address:",row.device_topic, "Email:",row.device_id)
