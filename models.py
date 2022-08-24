from sqlalchemy.sql.expression import false
from .database import Base
from sqlalchemy import Column,Integer, String , Boolean

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True,nullable= False)
    title = Column(String, nullable= False)
    description = Column(String, nullable= False)
    status = Column(Boolean, server_default='TRUE', nullable= False)