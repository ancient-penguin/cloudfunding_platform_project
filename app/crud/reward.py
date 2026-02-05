# app/crud/reward.py

from sqlalchemy.orm import Session
from app.models.reward import Reward
from app.schemas.reward import RewardCreate

# 리워드 생성
def create_reward(db: Session, reward: RewardCreate, project_id: int):
    db_reward = Reward(
        title=reward.title,
        description=reward.description,
        price=reward.price,
        stock=reward.stock,
        project_id=project_id, # 어떤 프로젝트의 물건인지 연결
        sold_count=0           # 처음엔 판매량 0
    )
    
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward

# 특정 프로젝트의 리워드 목록 조회
def get_rewards_by_project(db: Session, project_id: int):
    return db.query(Reward).filter(Reward.project_id == project_id).all()

# 리워드 단건 조회 (나중에 후원할 때 필요)
def get_reward(db: Session, reward_id: int):
    return db.query(Reward).filter(Reward.id == reward_id).first()