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

# user의 reward 조회 기능
def get_fundings_by_user(db: Session, user_id: int):
    return db.query(Funding).filter(Funding.user_id == user_id).all()

    from datetime import datetime

def cancel_funding(db: Session, funding_id: int, user_id: int):
    # 1. 후원 내역 찾기 (내 것인지 확인)
    funding = db.query(Funding).filter(Funding.id == funding_id, Funding.user_id == user_id).first()
    if not funding:
        raise HTTPException(status_code=404, detail="후원 내역을 찾을 수 없습니다.")

    # 2. 이미 취소된 건인지 확인
    if funding.status == 'cancelled':
        raise HTTPException(status_code=400, detail="이미 취소된 후원입니다.")

    # 3. 프로젝트 기간 확인 [핵심 로직!]
    project = db.query(Project).filter(Project.id == funding.project_id).first()
    if not project: # 혹시 프로젝트가 없으면
         raise HTTPException(status_code=404, detail="프로젝트가 존재하지 않습니다.")
         
    if datetime.now() > project.end_date:
        raise HTTPException(status_code=400, detail="프로젝트가 마감되어 취소할 수 없습니다.")

    # 4. 트랜잭션 시작 (3가지 동시 변경)
    try:
        # A. 리워드 재고 원복
        reward = db.query(Reward).filter(Reward.id == funding.reward_id).first()
        if reward:
            reward.sold_count -= 1
        
        # B. 프로젝트 모금액 차감
        project.current_amount -= funding.amount
        
        # C. 후원 상태 변경 ('cancelled') -> 삭제하지 않음!
        funding.status = 'cancelled'

        db.commit()
        db.refresh(funding)
        return funding

    except Exception as e:
        db.rollback()
        raise e