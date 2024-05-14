from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from datetime import datetime



Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(64))
    created_at = Column(DateTime, default=datetime.now)

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    password = Column(String)
    algorithm = Column(String)
    report_content = Column(String(255))
    is_cracked = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    time_taken = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)
    file = Column(Integer, ForeignKey('uploads.id'), nullable=True)

class Upload(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    path = Column(String)
    created_at = Column(DateTime, default=datetime.now)

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    feedback_content = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

class Vault(Base):
    __tablename__ = 'passvault'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    passfor = Column(String)
    password = Column(String)    
    created_at = Column(DateTime, default=datetime.now)

    



def get_db():
    engine = create_engine('sqlite:///pct.db')
    return sessionmaker(bind=engine)()

def save_to_db(object):
    db = get_db()      # open database
    db.add(object)     # insert object
    db.commit()        # save changes
    db.close()         # close database

#create database
if __name__ == "__main__":
    engine = create_engine('sqlite:///pct.db')
    Base.metadata.create_all(engine)
