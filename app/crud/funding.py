# app/crud/funding.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.funding import Funding
from app.models.reward import Reward
from app.models.project import Project
from app.schemas.funding import FundingCreate

def create_funding(db: Session, funding_in: FundingCreate, user_id: int):
    # 1. 리워드 정보 가져오기
    reward = db.query(Reward).filter(Reward.id == funding_in.reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="리워드를 찾을 수 없습니다.")

    # 2. 유효성 검사 (재고 & 가격) [Service Logic]
    # 남은 재고 계산
    remaining_stock = reward.stock - reward.sold_count
    if remaining_stock < 1:
        raise HTTPException(status_code=400, detail="품절된 리워드입니다.")
    
    if funding_in.amount < reward.price:
        raise HTTPException(status_code=400, detail="후원 금액이 리워드 가격보다 적습니다.")

    # 3. 프로젝트 정보 가져오기 (모금액 업데이트를 위해)
    project = db.query(Project).filter(Project.id == reward.project_id).first()
    
    # ---------------- 트랜잭션 시작 (여기서부터 DB 변경) ----------------
    try:
        # A. 후원 기록 생성
        db_funding = Funding(
            user_id=user_id,
            project_id=project.id,
            reward_id=reward.id,
            amount=funding_in.amount
        )
        db.add(db_funding)

        # B. 리워드 판매량 증가 (재고 차감 효과)
        reward.sold_count += 1
        
        # C. 프로젝트 모금액 증가
        project.current_amount += funding_in.amount

        # D. 모든 변경사항 확정 (Commit)
        db.commit()
        db.refresh(db_funding)
        return db_funding

    except Exception as e:
        db.rollback() # 에러 나면 모든 변경 취소!
        raise e