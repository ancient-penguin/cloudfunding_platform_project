from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    
    # FK: 어느 프로젝트의 리워드인가?
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    title = Column(String, nullable=False) 
    price = Column(Integer, nullable=False) 
    
    stock = Column(Integer, nullable=False) 
    sold_count = Column(Integer, default=0) 

    # 관계 설정
    project = relationship("Project", back_populates="rewards")
    fundings = relationship("Funding", back_populates="reward")