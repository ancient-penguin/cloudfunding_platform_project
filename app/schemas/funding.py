# app/schemas/funding.py

from pydantic import BaseModel, Field

#Funding은 수정되지 않는다.
#그렇기 때문에 따로 Base를 만들지 않고, 
#Create와 Response 각각의 기능에 집중할 수 있는 형태로 제작하는 것


# 1. 후원 요청 (Request)
class FundingCreate(BaseModel):
    reward_id: int
    amount: int = Field(..., gt=0, description="후원 금액은 0원보다 커야 합니다.")

# 2. 후원 응답 (Response)
class FundingResponse(BaseModel):
    id: int
    user_id: int
    project_id: int
    reward_id: int
    amount: int
    status: str = "success"

    class Config:
        from_attributes = True