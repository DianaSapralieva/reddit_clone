from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


# The base class will be the base for all the models we'll create.
Base = declarative_base()


####################
#### ORM Models ####
####################


# First class/model/Table
class BlogPost(Base):
    __tablename__ = "BlogPost" #table name in postgres

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    rating = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    writer_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    writer = relationship("User")

class User(Base):
    __tablename__ = "User" #table name in postgres

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

