from typing import Any, Union
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. 비밀번호 검증 함수 (로그인 할 때 사용)
# plain_password: 사용자가 입력한 비번
# hashed_password: DB에 암호화된 비밀번호
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 2. 비밀번호 암호화 함수 (회원가입 할 때 사용)
def get_password_hash(password):
    return pwd_context.hash(password)

# 3. 로그인 토큰 생성 
def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None):
    # 1) 유효시간 설정
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 2) 토큰에 담을 정보 / 만료시간, 이메일
    to_encode = {"exp" : expire, "sub" : str(subject)}

    # 3) 암호화 서명
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt