from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.crud.user import get_user_by_email

#1. 토큰을 어디서 가져올지 설정함(로그인 url 설정)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")

# 현재 유저를 반환하기 위함 > 지금 유저는 존재하는 유저인가? + 토큰
def get_current_user(
        token: str = Depends(oauth2_scheme), #헤더에서 토큰 추출
        db: Session = Depends(get_db)
) -> User:
    
    #인증이 실패한다면 보낼 에러 메시지 정의 / 401 자격 없음
    credentials_exception = HTTPException(  
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="자격 증명을 확인할 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try :
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        #get을 통해서 "sub"로 저장되어 있는 이메일을 가져옴. 없으면 None
        email: str = payload.get("sub")

        #이메일이 없는 상황
        if email is None:
            raise credentials_exception
    
    except JWTError:
        #토큰 형식이 잘못되었거나 위조된 경우
        raise credentials_exception
    
    #해독한 이메일을 바탕으로 유저가 존재하는지 확인
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    return user