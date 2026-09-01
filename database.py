from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database
from models import Base
from config import CONNECTION_STRING

def get_engine():
    engine=create_engine(CONNECTION_STRING, echo=False)
    return engine


def init_db():
    engine = get_engine()
    if not database_exists(engine.url):
        create_database(engine.url)
        print("Database created.")
    Base.metadata.create_all(engine)
    print("Database tables created.")
    return engine

def get_session(engine):
    session=sessionmaker(bind=engine)
    return session()

#Bugfix: Check engine and server connection
# eng1=get_engine()
# with eng1.connect() as conn:
#     result=conn.execute(text("SELECT 1"))
#     print(result.fetchone())
# print(eng1)