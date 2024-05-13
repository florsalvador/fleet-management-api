from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://default:Wd1enjQ2cHyL@ep-steep-paper-a4geq4k9-pooler.us-east-1.aws.neon.tech:5432/verceldb")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Taxis(Base):
    """..."""
    __tablename__ = "taxis"
    id = Column(Integer, primary_key=True)
    plate = Column(String)
    def __init__(self, plate):
        self.plate = plate
    # def __repr__(self):
    #     return f'Taxi({self.id}, {self.plate})'
    # def __str__(self):
    #     return self.id