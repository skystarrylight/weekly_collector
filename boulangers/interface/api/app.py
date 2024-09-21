# api/app.py

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from typing import List, Dict, Optional

from boulangers.application.services import IssueService
from boulangers.infrastructure.jira_client import JiraClient
from boulangers.domain.issue import Issue
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Static 파일 서빙 설정 (static 디렉토리 사용)
app.mount("/static", StaticFiles(directory="boulangers/static"), name="static")


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


# 기본 엔드포인트: index.html 페이지를 안내
@app.get("/")
async def read_root():
    return {"message": "Visit /static/index.html to view the frontend."}


# 에픽 조회 API
@app.get("/project/{project_key}/epics", response_model=List[Issue])
async def read_epics(project_key: str, issue_service: IssueService = Depends(get_issue_service)):
    try:
        return await issue_service.get_epics(project_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Task 조회 API
@app.get("/project/{project_key}/tasks", response_model=List[Issue])
async def read_tasks(project_key: str, issue_service: IssueService = Depends(get_issue_service)):
    try:
        return await issue_service.get_tasks(project_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Sub-task 조회 API
@app.get("/project/{project_key}/subtasks", response_model=List[Issue])
async def read_subtasks(project_key: str, issue_service: IssueService = Depends(get_issue_service)):
    try:
        return await issue_service.get_subtasks(project_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Story 조회 API
@app.get("/project/{project_key}/stories", response_model=List[Issue])
async def read_stories(project_key: str, issue_service: IssueService = Depends(get_issue_service)):
    try:
        return await issue_service.get_stories(project_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 에픽 계층 구조 조회 API
@app.get("/project/{project_key}/hierarchy", response_model=Dict)
async def read_project_hierarchy(
        project_key: str,
        jql_query: Optional[str] = Query(None),
        issue_service: IssueService = Depends(get_issue_service)
):
    """
    프로젝트 코드 기준으로 에픽 및 각 에픽에 연결된 Task와 Sub-task의 계층 구조를 반환
    """
    try:
        # 프로젝트 내 모든 에픽을 조회
        epics = await issue_service.get_epics(project_key, jql_query)
        project_hierarchy = {}

        # 각 에픽에 대한 계층 구조 생성
        for epic in epics:
            hierarchy = await issue_service.get_epic_with_hierarchy(epic.key, jql_query)
            project_hierarchy[epic.key] = hierarchy

        return project_hierarchy

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
