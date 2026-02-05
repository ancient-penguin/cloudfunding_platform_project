from pydantic import BaseModel, Field, validator
from typing import Optional

# 1. 공통 속성
class RewardBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: int = Field(..., gt=0, description="가격은 0원보다 커야 합니다.")
    stock: int = Field(..., gt=0, description="재고는 1개 이상이어야 합니다.")

# 2. 생성 요청 (Request)
class RewardCreate(RewardBase):
    pass

# 3. 응답 데이터 (Response)
class RewardResponse(RewardBase):
    id: int
    project_id: int
    sold_count: int
    remaining_stock: int  # 남은 수량을 계산해서 줄 필드

    # 남은 수량 계산 로직 (stock - sold_count)
    @validator('remaining_stock', always=True, pre=True)
    def calculate_remaining(cls, v, values):
        # DB 모델에서 stock과 sold_count를 가져와 계산
        stock = values.get('stock', 0)
        sold_count = values.get('sold_count', 0)
        return stock - sold_count

    class Config:
        from_attributes = True
        