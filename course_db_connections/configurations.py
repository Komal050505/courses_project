import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_connection_url = "postgresql://postgres:1995@localhost:5432/postgres"

engine = create_engine(url=database_connection_url, echo=True)
conn = engine.connect()

# Creating a database session
Session = sessionmaker(bind=engine)
session = Session()
