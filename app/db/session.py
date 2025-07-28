from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(settings.DATABASE_URL)
sessionlocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)


def get_db():
    db = sessionlocal
    try:
        yield db
    finally:
        db.close()