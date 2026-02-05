# app/api/v1/endpoints/reward.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.reward import RewardCreate, RewardResponse
from app.crud import reward as crud_reward
from app.crud import project as crud_project # 프로젝트 주인 확인용

router = APIRouter()

# 1. 리워드 생성 (특정 프로젝트에 리워드 추가)
@router.post("/{project_id}/rewards", response_model=RewardResponse, status_code=status.HTTP_201_CREATED)
def create_reward(
    project_id: int,
    reward_in: RewardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # A. 프로젝트가 실제로 존재하는지 확인
    project = crud_project.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")

    # B. 권한 체크: 로그인한 사람이 프로젝트 주인인가? [Service Logic: 권한 체크]
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="본인의 프로젝트에만 리워드를 등록할 수 있습니다.")

    # C. 리워드 생성
    return crud_reward.create_reward(db=db, reward=reward_in, project_id=project_id)


# 2. 특정 프로젝트의 리워드 목록 조회 (누구나 가능)
@router.get("/{project_id}/rewards", response_model=List[RewardResponse])
def read_rewards(
    project_id: int,
    db: Session = Depends(get_db)
):
    # 프로젝트 존재 여부 확인 (친절한 에러 메시지를 위해)
    project = crud_project.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")
        
    return crud_reward.get_rewards_by_project(db, project_id=project_id)