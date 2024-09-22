# api/app.py

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import FileResponse
from typing import List, Dict, Optional

from boulangers.application.services import IssueService
from boulangers.infrastructure.jira_client import JiraClient
from boulangers.domain.issue import Issue
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 리액트 빌드된 정적 파일을 서빙
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")


# IssueService 생성 함수
def get_issue_service() -> IssueService:
    domain = os.getenv('JIRA_DOMAIN')
    email = os.getenv('JIRA_EMAIL')
    api_token = os.getenv('JIRA_API_TOKEN')
    epic_field = os.getenv('JIRA_EPIC_FIELD', '"Epic Link"')

    if not all([domain, email, api_token]):
        raise ValueError("Jira 인증 정보가 설정되어 있지 않습니다.")

    jira_client = JiraClient(domain, email, api_token, epic_field)
    issue_service = IssueService(jira_client)
    return issue_service


def _clean_assignees(assignees: Optional[List[str]]) -> Optional[List[str]]:
    if not assignees or all(a == '' for a in assignees):
        return None
    return assignees


# 기본 엔드포인트로 리액트의 index.html 제공
@app.get("/")
async def serve_frontend():
    return FileResponse('frontend/build/index.html')


# 에픽 조회 API
@app.get("/project/{project_key}/epics", response_model=List[Issue])
async def read_epics(
        project_key: str,
        assignees: Optional[List[str]] = Query(None),
        issue_service: IssueService = Depends(get_issue_service)
):
    try:
        assignees = _clean_assignees(assignees)
        return await issue_service.get_epics(project_key, assignees)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Task 조회 API
@app.get("/project/{project_key}/tasks", response_model=List[Issue])
async def read_tasks(
        project_key: str,
        assignees: Optional[List[str]] = Query(None),
        issue_service: IssueService = Depends(get_issue_service)
):
    try:
        assignees = _clean_assignees(assignees)
        return await issue_service.get_tasks(project_key, assignees)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Sub-task 조회 API
@app.get("/project/{project_key}/subtasks", response_model=List[Issue])
async def read_subtasks(
        project_key: str,
        assignees: Optional[List[str]] = Query(None),
        issue_service: IssueService = Depends(get_issue_service)
):
    try:
        assignees = _clean_assignees(assignees)
        return await issue_service.get_subtasks(project_key, assignees)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Story 조회 API
@app.get("/project/{project_key}/stories", response_model=List[Issue])
async def read_stories(
        project_key: str,
        assignees: Optional[List[str]] = Query(None),
        issue_service: IssueService = Depends(get_issue_service)
):
    try:
        assignees = _clean_assignees(assignees)
        return await issue_service.get_stories(project_key, assignees)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 에픽 계층 구조 조회 API
@app.get("/project/{project_key}/hierarchy", response_model=Dict)
async def read_project_hierarchy(
        project_key: str,
        assignees: Optional[List[str]] = Query(None),
        issue_service: IssueService = Depends(get_issue_service)
):
    """
    프로젝트 코드 기준으로 에픽 및 각 에픽에 연결된 Task와 Sub-task의 계층 구조를 반환
    """
    try:
        assignees = _clean_assignees(assignees)
        hierarchy = await issue_service.get_hierarchical_issues(project_key, assignees)
        return hierarchy
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
