from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Funding(Base):
    __tablename__ = "fundings"

    id = Column(Integer, primary_key=True, index=True)
    
    # FK 3대장 (누가, 어디에, 무엇을)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    reward_id = Column(Integer, ForeignKey("rewards.id"))
    
    amount = Column(Integer, nullable=False) # 실제 결제 금액
    status = Column(String, default="pledged") # pledged(참여), paid(완료), cancelled(취소)
    
    pledged_at = Column(DateTime(timezone=True), server_default=func.now()) # 후원 시간 자동생성

    # 관계 설정 (객체로 접근하기 위함)
    backer = relationship("User", back_populates="fundings")
    project = relationship("Project", back_populates="fundings")
    reward = relationship("Reward", back_populates="fundings")