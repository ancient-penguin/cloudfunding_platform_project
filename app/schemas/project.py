from pydantic import BaseModel, validator, Field
from datetime import datetime
from typing import Optional

# 1. 공통으로 사용할 기본 속성
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    target_amount: int = Field(..., gt=0, description="목표 금액은 0원보다 커야 합니다.")
    start_date: datetime
    end_date: datetime

# 2. 프로젝트 생성 시 받을 데이터 (Request)
class ProjectCreate(ProjectBase):
    # 날짜 검증 로직 (Service Logic: 날짜 검증)
    @validator('end_date')
    def check_dates(cls, v, values):
        # start_date가 먼저 입력되었는지 확인
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('종료일은 시작일 이후여야 합니다.')
        return v

# 3. 사용자에게 보여줄 데이터 (Response)
class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    current_amount: int
    status: str

    class Config:
        # DB 모델(ORM)을 Pydantic 모델로 변환하기 위해 필수
        from_attributes = True