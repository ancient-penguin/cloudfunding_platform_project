from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    full_name = Column(String, nullable=True) 
    is_active = Column(Boolean, default=True)
    
    role = Column(String, default="user") #'user or 'admin

    #realation setting
    #back_populate : 상대방 쪽에서 호칭할 때 쓸 이름
    projects = relationship("Project", back_populates="creator")
    fundings = relationship("Funding", back_populates="backer")
