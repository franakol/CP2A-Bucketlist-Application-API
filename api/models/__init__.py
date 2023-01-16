from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine("postgresql://afran:123@localhost:5432/db")


Base = declarative_base()
metadata = Base.metadata

SessionLocal=sessionmaker(bind=engine)
