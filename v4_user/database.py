from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# Database URL (Bad practice to put it here)
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}/{settings.database_name}"

#Running engine for ORM translation (python to SQL)
database_engine = create_engine(DATABASE_URL)

#session template for the connection
SessionTemplate = sessionmaker(
    autocommit=False, autoflush=False, bind=database_engine)

#Create and close session on-demand
def get_db():
    db = SessionTemplate()
    try:
        yield db
    finally:
        db.close()