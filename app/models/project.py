from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    target_amount = Column(Integer, nullable=False)
    current_amount = Column(Integer, default=0)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    status = Column(String, default="ongoing") # ongoing, success, fail

    #relationship setting
    creator = relationship("User", back_populates="projects") # 만든 사람
    rewards = relationship("Reward", back_populates="project") # 리워드 목록
    fundings = relationship("Funding", back_populates="project") # 후원 내역들
