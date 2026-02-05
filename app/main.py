from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine

from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.login import router as login_router
from app.api.v1.endpoints.project import router as project_router
from app.api.v1.endpoints.reward import router as reward_router

app = FastAPI()

# 1. 서버 시작 시 DB 연결 테스트 (Startup Event)
# 서버가 켜질 때 딱 한 번 실행되는 함수입니다.
@app.on_event("startup")
def check_db_connection():
    try:
        # 엔진을 통해 DB와 연결을 시도하고, 간단한 질의(SELECT 1)를 보냅니다.
        # SELECT 1은 DB가 살아있는지 확인하는 가장 가벼운 명령어입니다.
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("\n✅✅✅ 데이터베이스 연결 성공! (PostgreSQL) ✅✅✅\n")
    except Exception as e:
        print("\n❌❌❌ 데이터베이스 연결 실패! ❌❌❌")
        print(f"에러 내용: {e}\n")

#라우터 추가
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(login_router, tags=["login"])
app.include_router(project_router, prefix="/projects", tags=["projects"])
app.include_router(reward_router, prefix="/projects", tags=["rewards"])

# 2. 기본 페이지 (Health Check 용)
@app.get("/")
def read_root():
    return {"message": "Welcome to My Funding Service!"}