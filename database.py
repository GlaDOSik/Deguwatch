from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from vial.config import app_config
import dw_configuration

engine = create_engine(app_config.get(dw_configuration.DB_CONNECTION_STRING))
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
