from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def create_user(db: Session, user: UserCreate):
    # 1. 비밀번호 암호화
    hashed_password = get_password_hash(user.password)
    
    # 2. DB 모델 객체 생성
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    
    # 3. DB에 추가하고 커밋(저장)
    db.add(db_user)
    db.commit()
    
    # 4. 방금 저장된 정보를 다시 새로고침해서 가져옴 (ID 등이 생성되었으므로)
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    # 이메일로 이미 가입된 회원이 있는지 찾을 때 씁니다.
    return db.query(User).filter(User.email == email).first()