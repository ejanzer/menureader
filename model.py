from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///menureader.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()


def main():
    # Uncomment and run model.py as main to create schema
   # Base.metadata.create_all(engine) 

if __name__ == "__main__":
    main()