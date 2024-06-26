from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from .database import base
from sqlalchemy import table,Column
from sqlalchemy.sql.expression import null

class POST (base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Votes(base):
    __tablename__ = "votes"
    user_id = Column(Integer,  ForeignKey("users.id", ondelete="CASCADE"), primary_key=True,)
    post_id = Column(Integer,  ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True,)
        
