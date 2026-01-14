from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.core import security
from app.core.config import settings
from app.crud import user as crud_user
from app.db.session import get_db

router = APIRouter()

@router.route("/login/access-token")
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    
    # 1) 이메일로 유저 찾기
    user = crud_user.get_user_by_email(db, email=form_data.username)

    # 2) 유저가 없거나 비밀번호가 틀리면 에러 발생 (401)
    if not user or not security.verify_password(form_data.password, user.hashed_password) :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 정확하지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3) 토큰 유효기간 설정
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 4) JWT 토큰 발급
    access_token = security.create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    # 5) 최종 응답 (입장권 전달)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
