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