# app/api/v1/endpoints/funding.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.funding import FundingCreate, FundingResponse
from app.crud import funding as crud_funding

router = APIRouter()

@router.post("/", response_model=FundingResponse)
def create_funding(
    funding_in: FundingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    새로운 후원을 생성합니다.
    - 리워드 재고가 차감됩니다.
    - 프로젝트 모금액이 증가합니다.
    """
    return crud_funding.create_funding(db=db, funding_in=funding_in, user_id=current_user.id)

@router.post("/{funding_id}/cancel", response_model=FundingResponse)
def cancel_funding(
    funding_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    특정 후원 내역을 취소합니다.
    - 프로젝트 마감일 이전일 때만 가능합니다.
    - 데이터는 삭제되지 않고 상태가 'cancelled'로 변경됩니다.
    """
    return crud_funding.cancel_funding(db=db, funding_id=funding_id, user_id=current_user.id)