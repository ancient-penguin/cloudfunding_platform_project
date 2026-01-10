from fastapi import FastAPI

app = FastAPI(
    title="Crowd Funding API",
    version="1.0.0",
    description="크라우드 펀딩 플랫폼 백엔드 API"
)

@app.get("/")
def read_root():
    return {"message": "Hello, Crowd Funding!"}

# 나중에 여기에 DB 연결과 라우터를 추가할 예정