# app/api/v1/endpoints/project.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse
from app.crud import project as crud_project

router = APIRouter()

# 1. 프로젝트 생성 (로그인 필요)
@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 토큰을 검사해 유저를 가져옴
):
    """
    새로운 프로젝트를 생성합니다.
    - 로그인한 유저만 가능합니다.
    - user_id는 토큰에서 추출하여 자동으로 연결됩니다.
    """
    return crud_project.create_project(db=db, project=project_in, user_id=current_user.id)

# 2. 프로젝트 목록 조회 (로그인 불필요 - 누구나 조회 가능)
@router.get("/", response_model=List[ProjectResponse])
def read_projects(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    전체 프로젝트 목록을 조회합니다.
    """
    projects = crud_project.get_projects(db, skip=skip, limit=limit)
    return projects

# 3. 프로젝트 상세 조회
@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = crud_project.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")
    return project