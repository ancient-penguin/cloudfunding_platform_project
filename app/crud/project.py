# app/crud/project.py

from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate

# 프로젝트 생성
def create_project(db: Session, project: ProjectCreate, user_id: int):
    # 1. 스키마 데이터를 딕셔너리로 변환 (project.dict())
    # 2. user_id를 추가하여 DB 모델 객체 생성
    db_project = Project(
        title=project.title,
        description=project.description,
        target_amount=project.target_amount,
        start_date=project.start_date,
        end_date=project.end_date,
        user_id=user_id  # <--- 핵심: 로그인한 유저의 ID를 주입 [Service Logic: 생성자 연결]
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# 프로젝트 단건 조회
def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

# 프로젝트 목록 조회 (여러 개)
def get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Project).offset(skip).limit(limit).all()