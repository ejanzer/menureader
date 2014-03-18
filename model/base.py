from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///menureader.db", echo=False)
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = db_session.query_property()