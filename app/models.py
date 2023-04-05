from sqlalchemy.engine import URL
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base,relationship,sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

url = URL.create(
    drivername = "postgresql",
    username = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    host = os.getenv("DB_HOST"),
    database = os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT"),
)

engine = create_engine(url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# session = Session()

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

class UserAccount(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'), nullable=False, index=True)
    user = relationship("UserAccount", backref='blogs')

# Base.metadata.create_all(engine)