import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 1. .env 파일에 있는 변수들을 읽어옵니다.
    # (변수 이름이 .env와 똑같아야 자동으로 매칭됩니다)
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    
    SECRET_KEY: str
    ALGORITHM: str

    # 2. 읽어온 정보로 'DB 접속 주소(URL)'를 조립합니다.
    # 형태: postgresql://아이디:비번@주소:포트/DB이름
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # 3. 설정: ".env 파일을 찾아서 읽으세요" 라고 지시
    class Config:
        env_file = ".env"

# 이 객체(settings)를 불러오면 바로 환경변수 값을 쓸 수 있습니다.
settings = Settings()