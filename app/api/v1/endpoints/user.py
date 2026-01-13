from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserResponse
from app.db.session import get_db

router = APIRouter()

#회원가입 엔드포인트
#status_code = 201 : 생성완료
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    #이메일 중복 검사
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")

    #유저 생성
    return crud_user.create_user(db=db, user=user)