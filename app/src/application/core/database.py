from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_continuum import make_versioned

from src.application.core import config

SQLALCHEMY_DATABASE_URL = config.settings.database_url

make_versioned(user_cls=None)

if config.settings.environment == "development":
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if config.settings.environment == "development":
    import sqlalchemy.event as sqlevent

    sqlevent.listen(engine, 'connect',
                    lambda conn, rec: conn.execute('PRAGMA foreign_keys=ON;'))

Base = declarative_base()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
