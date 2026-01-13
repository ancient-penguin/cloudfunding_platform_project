from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

#회원가입할 때 필요한 정보(create)
class UserCreate(UserBase):
    password: str
    full_name: str | None = None
    role: str = "user" # 기본값은 일반 유저 user or admin


#사용자에게 정보를 돌려줄 때 사용하는 양식(response)
class UserResponse(UserBase):
    id: int
    full_name: str | None = None
    is_active: bool
    role: str

    class Config:
        # ORM(SQLAlchemy) 객체를 Pydantic 모델로 읽을 수 있게 해주는 설정
        from_attributes = True
