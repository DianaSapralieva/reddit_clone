from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL (Bad practice to put it here)
DATABASE_URL = "postgresql://postgres:API@localhost/reddit_clone_manytomany"

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