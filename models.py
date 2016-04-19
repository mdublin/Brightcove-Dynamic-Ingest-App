from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime

engine = create_engine(
                       'postgresql://mdublin1:buggy123123@localhost:5432/Brightcove-Dynamic-Ingest-App')
Session = sessionmaker(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime


class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True)
    video_name = Column(String, nullable=True)
    #description = Column(String)
    BCid = Column(String, nullable=True)
    DynamicIngest_response = Column(String, nullable=True)
    Source_URL = Column(String, nullable=True)
    stored = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
