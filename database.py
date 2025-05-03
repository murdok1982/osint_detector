from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    username = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    evaluation = Column(String)

engine = create_engine('sqlite:///osint.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_message(user_id, username, message, evaluation):
    msg = Message(user_id=user_id, username=username, message=message, evaluation=evaluation)
    session.add(msg)
    session.commit()
