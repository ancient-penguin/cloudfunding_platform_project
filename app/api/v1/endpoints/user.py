from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import user as crud_user
from app.crud import project as crud_project
from app.crud import funding as crud_funding
from app.schemas.user import UserCreate, UserResponse
from app.schemas.project import ProjectResponse
from app.schemas.funding import FundingResponse
from app.models import User
from app.db.session import get_db
from app.api.deps import get_current_user

router = APIRouter()

#회원가입 엔드포인트
#status_code = 201 : 생성완료
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    #이메일 중복 검사
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")

    #유저 생성
    return crud_user.create_user(db=db, user=user)

#내 정보 조회
@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_user)
):  
    '''
    현재 로그인한 유저의 정보를 가져옴. 토큰이 없거나 유효하지 않으면 401
    current_user는 sqlalchemy를 통해 작업된 model 형태의 객체임. 그렇기 때문에 models에서 import
    current_user가 왜 파라미터로 포함되어 들어갔는가? 애초에 Depends는 함수의 파라미터 인가를 넣을 때만 사용가능
    '''
    return current_user

#내가 만든 프로젝트 조회
@router.get("/me/projects", response_model=List[ProjectResponse])
def read_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) :
    projects = crud_project.get_projects_by_user(db, user_id=current_user.id)
    return projects

#내가 후원한 내역 조회
@router.get("/me/fundings", response_model=List[FundingResponse])
def read_my_fundings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fundings = crud_funding.get_fundings_by_user(db, user_id=current_user.id)
    return fundings