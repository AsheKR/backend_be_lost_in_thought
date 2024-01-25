from core.config import get_config
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

config = get_config()
engine: Engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
