from typing import List, Dict, Optional
from boulangers.domain.issue import Issue
from boulangers.application.ports import IssueRepositoryPort


class IssueService:
    def __init__(self, repository: IssueRepositoryPort):
        self.repository = repository

    # 에픽 조회
    async def get_epics(self, project_key: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """
        특정 프로젝트의 모든 에픽을 조회, 추가적인 JQL 조건을 적용할 수 있음
        """
        jql_query = f'project = "{project_key}" AND issuetype = "Epic"'
        if additional_jql:
            jql_query += f" {additional_jql}"
        return await self.repository.fetch_issues(jql_query)

    # 태스크 조회
    async def get_tasks(self, project_key: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """
        특정 프로젝트의 모든 Task를 조회, 추가적인 JQL 조건을 적용할 수 있음
        """
        jql_query = f'project = "{project_key}" AND issuetype = "Task"'
        if additional_jql:
            jql_query += f" {additional_jql}"
        return await self.repository.fetch_issues(jql_query)

    # 서브태스크 조회
    async def get_subtasks(self, project_key: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """
        특정 프로젝트의 모든 Sub-task를 조회, 추가적인 JQL 조건을 적용할 수 있음
        """
        jql_query = f'project = "{project_key}" AND issuetype = "Sub-task"'
        if additional_jql:
            jql_query += f" {additional_jql}"
        return await self.repository.fetch_issues(jql_query)

    # 스토리 조회
    async def get_stories(self, project_key: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """
        특정 프로젝트의 모든 Story를 조회, 추가적인 JQL 조건을 적용할 수 있음
        """
        jql_query = f'project = "{project_key}" AND issuetype = "Story"'
        if additional_jql:
            jql_query += f" {additional_jql}"
        return await self.repository.fetch_issues(jql_query)

    # 에픽에 연결된 태스크 조회
    async def get_tasks_by_epic(self, epic_key: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """
        특정 에픽에 연결된 모든 Task를 조회, 추가적인 JQL 조건을 적용할 수 있음
        """
        jql_query = f'"Epic Link" = "{epic_key}"'
        if additional_jql:
            jql_query += f" {additional_jql}"
        print(jql_query)
        tasks = await self.repository.fetch_issues(jql_query)
        print(tasks)
        return tasks

    # 태스크에 연결된 서브태스크 조회
    async def get_subtasks_by_task(self, task_key: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """
        특정 Task에 연결된 모든 Sub-task를 조회, 추가적인 JQL 조건을 적용할 수 있음
        """
        jql_query = f'parent = "{task_key}"'
        if additional_jql:
            jql_query += f" {additional_jql}"
        subtasks = await self.repository.fetch_issues(jql_query)
        return subtasks

    # 에픽과 하위 구조 조회
    async def get_epic_with_hierarchy(self, epic_key: str, additional_jql: Optional[str] = None) -> Dict:
        """
        특정 에픽에 연결된 Task 및 각 Task에 연결된 Sub-task를 추가적인 JQL 조건과 함께 계층 구조로 반환
        """
        # 에픽에 연결된 Task 조회
        tasks = await self.get_tasks_by_epic(epic_key, additional_jql)

        # 각 Task에 연결된 Sub-task 조회
        task_with_subtasks = []
        for task in tasks:
            subtasks = await self.get_subtasks_by_task(task.key, additional_jql)
            task_with_subtasks.append({
                "task": task,
                "subtasks": subtasks
            })

        # 에픽과 Task, Sub-task 계층 구조 반환
        return {
            "epic": epic_key,
            "tasks": task_with_subtasks
        }
