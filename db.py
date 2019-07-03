"""Create db module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.base_config import Config


ENGINE = create_engine(Config.SQLALCHEMY_DATABASE_URI)

BASE = declarative_base()

SESSION = sessionmaker(bind=ENGINE)
SESSION = SESSION()
