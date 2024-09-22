from typing import List, Dict, Optional
from boulangers.domain.issue import Issue
from boulangers.application.ports import IssueRepositoryPort


class IssueService:
    def __init__(self, repository: IssueRepositoryPort):
        self.repository = repository

    async def get_issues_by_type_and_assignee(
            self,
            project_key: str,
            issue_type: Optional[str],
            assignees: List[str],
            additional_jql: Optional[str] = None
    ) -> List[Issue]:
        """
        특정 프로젝트의 이슈를 타입과 담당자에 따라 조회, 추가적인 JQL 조건을 적용할 수 있음
        """
        jql_query = f'project = "{project_key}"'

        # Issue 타입 필터 추가
        print(issue_type)
        if issue_type:
            jql_query += f' AND issuetype = "{issue_type}"'

        # Assignee 필터 추가
        print(bool(assignees))
        print(assignees)
        if assignees:
            assignee_filter = ' OR '.join([f'assignee = "{assignee}"' for assignee in assignees])
            jql_query += f' AND ({assignee_filter})'

        # 추가적인 JQL 조건이 있을 경우 추가
        print(additional_jql)
        if additional_jql:
            jql_query += f" {additional_jql}"
        print("=======================")
        print(jql_query)
        print("=======================")
        return await self.repository.fetch_issues(jql_query)

    # 에픽 조회
    async def get_epics(self, project_key: str, assignees: List[str], additional_jql: Optional[str] = None) -> List[Issue]:
        return await self.get_issues_by_type_and_assignee(project_key, "Epic", assignees, additional_jql)

    # 태스크 조회
    async def get_tasks(self, project_key: str, assignees: List[str], additional_jql: Optional[str] = None) -> List[Issue]:
        return await self.get_issues_by_type_and_assignee(project_key, "Task", assignees, additional_jql)

    # 서브태스크 조회
    async def get_subtasks(self, project_key: str, assignees: List[str], additional_jql: Optional[str] = None) -> List[Issue]:
        return await self.get_issues_by_type_and_assignee(project_key, "Subtask", assignees, additional_jql)

    # 스토리 조회
    async def get_stories(self, project_key: str, assignees: List[str], additional_jql: Optional[str] = None) -> List[Issue]:
        return await self.get_issues_by_type_and_assignee(project_key, "Story", assignees, additional_jql)

    # 계층 구조 조회
    async def get_hierarchical_issues(self, project_key: str, assignees: List[str], additional_jql: Optional[str] = None) -> Dict[str, Dict]:
        """
        에픽, 태스크, 서브태스크 계층 구조로 이슈들을 반환
        """
        try:
            # 모든 이슈를 조회
            issues = await self.get_issues_by_type_and_assignee(project_key, None, assignees, additional_jql)

            # 에픽, 태스크, 서브태스크를 담을 딕셔너리
            epic_hierarchy = {}
            task_map = {}
            subtask_map = {}

            # 이슈들을 타입별로 그룹화
            epics = [issue for issue in issues if issue.type == 'Epic']
            tasks = [issue for issue in issues if issue.type == 'Task']
            subtasks = [issue for issue in issues if issue.type == 'Subtask']

            # 1. 에픽을 먼저 처리
            for epic in epics:
                self._add_epic(epic, epic_hierarchy)

            # 2. 태스크를 처리하여 해당 에픽에 추가
            for task in tasks:
                self._add_task(task, epic_hierarchy, task_map)

            # 3. 서브태스크를 처리하여 해당 태스크에 추가
            for subtask in subtasks:
                self._add_subtask(subtask, task_map, subtask_map)
            print(epic_hierarchy)
            return epic_hierarchy

        except Exception as e:
            print(f"Error in get_hierarchical_issues: {e}")
            raise e

    @staticmethod
    def _add_epic(issue, epic_hierarchy):
        """에픽을 계층 구조에 추가"""
        if issue.key not in epic_hierarchy:
            epic_hierarchy[issue.key] = {
                'summary': issue.summary,
                'status': issue.status,
                'assignee': issue.assignee if issue.assignee else 'Unassigned',
                'type': issue.type,  # 이슈 타입 추가
                'due_date': issue.due_date,  # 종료일자 추가
                'tasks': {}
            }

    @staticmethod
    def _add_task(issue, epic_hierarchy, task_map):
        """태스크를 에픽 하위에 추가"""
        parent_key = issue.parent  # 부모 이슈 (에픽 키)
        if parent_key in epic_hierarchy:
            if issue.key not in task_map:
                task_map[issue.key] = {
                    'summary': issue.summary,
                    'status': issue.status,
                    'assignee': issue.assignee if issue.assignee else 'Unassigned',
                    'type': issue.type,  # 이슈 타입 추가
                    'due_date': issue.due_date,  # 종료일자 추가
                    'subtasks': {}
                }
            # 태스크가 에픽 하위에 속하는지 부모 키를 비교하고 추가
            epic_hierarchy[parent_key]['tasks'][issue.key] = task_map[issue.key]

    @staticmethod
    def _add_subtask(issue, task_map, subtask_map):
        """서브태스크를 태스크 하위에 추가"""
        parent_key = issue.parent  # 부모 이슈 (태스크 키)
        if parent_key in task_map:
            if issue.key not in subtask_map:
                subtask_map[issue.key] = {
                    'summary': issue.summary,
                    'status': issue.status,
                    'assignee': issue.assignee if issue.assignee else 'Unassigned',
                    'type': issue.type,  # 이슈 타입 추가
                    'due_date': issue.due_date,  # 종료일자 추가
                }
            task_map[parent_key]['subtasks'][issue.key] = subtask_map[issue.key]
