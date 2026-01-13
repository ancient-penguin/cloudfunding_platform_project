from app.db.session import engine
from app.db.base import Base
from app import models

def create_tables():
    print("테이블 생성 시작...")
    Base.metadata.create_all(bind=engine)
    print("모든 테이블 생성 완료!")

if __name__ == "__main__":
    create_tables()