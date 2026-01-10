from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. 엔진 생성 
engine = create_engine(settings.DATABASE_URL)

# 2. 세션 만들기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. 의존성 함수 (Dependency) 
def get_db():
    db = SessionLocal()  # 1) 세션 연결
    try:
        yield db         # 2) 연결을 API에게 빌려줌
    finally:
        db.close()       # 3) 완료하면 무조건 단절