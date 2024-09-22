from typing import List, Dict, Optional
from boulangers.domain.issue import Issue
from boulangers.application.ports import IssueRepositoryPort


class IssueService:
    def __init__(self, repository: IssueRepositoryPort) -> None:
        """IssueService 클래스 초기화."""
        self.repository = repository

    async def get_issues_by_type(self, project_key: str, issue_type: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """
        특정 프로젝트의 이슈를 타입별로 조회, 추가적인 JQL 조건을 적용할 수 있음.

        Args:
            project_key (str): Jira 프로젝트 키.
            issue_type (str): 조회할 이슈 타입 (예: 'Epic', 'Task', 'Subtask').
            additional_jql (Optional[str]): 추가 JQL 조건.

        Returns:
            List[Issue]: 조회된 이슈 리스트.
        """
        jql_query = f'project = "{project_key}" AND issuetype = "{issue_type}"'
        if additional_jql:
            jql_query += f" {additional_jql}"
        return await self.repository.fetch_issues(jql_query)

    async def get_epics(self, project_key: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """에픽 이슈 조회."""
        return await self.get_issues_by_type(project_key, "Epic", additional_jql)

    async def get_tasks(self, project_key: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """태스크 이슈 조회."""
        return await self.get_issues_by_type(project_key, "Task", additional_jql)

    async def get_subtasks(self, project_key: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """서브태스크 이슈 조회."""
        return await self.get_issues_by_type(project_key, "Subtask", additional_jql)

    async def get_stories(self, project_key: str, additional_jql: Optional[str] = None) -> List[Issue]:
        """스토리 이슈 조회."""
        return await self.get_issues_by_type(project_key, "Story", additional_jql)

    async def get_hierarchical_issues(self, project_key: str) -> Dict[str, Dict]:
        """
        에픽, 태스크, 서브태스크 계층 구조로 이슈들을 반환.

        Args:
            project_key (str): 프로젝트 키.

        Returns:
            Dict[str, Dict]: 계층 구조를 나타내는 이슈 딕셔너리.
        """
        try:
            issues = await self.repository.fetch_issues(f'project = "{project_key}"')

            epic_hierarchy = {}
            task_map = {}
            subtask_map = {}

            # 이슈들을 타입별로 그룹화
            grouped_issues = self._group_issues_by_type(issues)

            # 에픽, 태스크, 서브태스크 추가
            self._process_issues(grouped_issues['Epic'], epic_hierarchy, task_map, subtask_map, 'tasks')
            self._process_issues(grouped_issues['Task'], epic_hierarchy, task_map, subtask_map, 'subtasks', 'parent')
            self._process_issues(grouped_issues['Subtask'], task_map, subtask_map, subtask_map, 'subtasks', 'parent')

            return epic_hierarchy

        except Exception as e:
            print(f"Error in get_hierarchical_issues: {e}")
            raise e

    @staticmethod
    def _group_issues_by_type(issues: List[Issue]) -> Dict[str, List[Issue]]:
        """
        이슈를 타입별로 그룹화.

        Args:
            issues (List[Issue]): 이슈 리스트.

        Returns:
            Dict[str, List[Issue]]: 타입별로 그룹화된 이슈 딕셔너리.
        """
        grouped_issues = {'Epic': [], 'Task': [], 'Subtask': []}
        for issue in issues:
            if issue.type == 'Epic':
                grouped_issues['Epic'].append(issue)
            elif issue.type == 'Task':
                grouped_issues['Task'].append(issue)
            elif issue.type == 'Subtask':
                grouped_issues['Subtask'].append(issue)
        return grouped_issues

    @staticmethod
    def _process_issues(issues: List[Issue], parent_map: Dict, issue_map: Dict, sub_map: Dict, child_key: str, parent_key: Optional[str] = None) -> None:
        """
        이슈를 부모-자식 관계에 따라 계층 구조에 추가.

        Args:
            issues (List[Issue]): 이슈 리스트.
            parent_map (Dict): 부모 이슈 맵.
            issue_map (Dict): 추가될 이슈 맵.
            sub_map (Dict): 하위 이슈 맵.
            child_key (str): 하위 이슈를 저장할 키 ('tasks' 또는 'subtasks').
            parent_key (Optional[str]): 부모 이슈 키 (예: 'parent').
        """
        for issue in issues:
            parent_id = getattr(issue, parent_key) if parent_key else None
            if parent_key and parent_id and parent_id in parent_map:
                IssueService._add_to_hierarchy(issue, parent_map[parent_id][child_key], issue_map, sub_map, child_key)
            else:
                IssueService._add_to_hierarchy(issue, parent_map, issue_map, sub_map, child_key)

    @staticmethod
    def _add_to_hierarchy(issue: Issue, hierarchy: Dict, issue_map: Dict, sub_map: Dict, child_key: str) -> None:
        """
        이슈를 계층 구조에 추가.

        Args:
            issue (Issue): 추가할 이슈.
            hierarchy (Dict): 계층 구조 딕셔너리.
            issue_map (Dict): 추가될 이슈 맵.
            sub_map (Dict): 하위 이슈 맵.
            child_key (str): 하위 이슈를 저장할 키 ('tasks' 또는 'subtasks').
        """
        if issue.key not in hierarchy:
            hierarchy[issue.key] = {
                'summary': issue.summary,
                'status': issue.status,
                'assignee': issue.assignee if issue.assignee else 'Unassigned',
                'reporter': issue.reporter,
                'priority': issue.priority,
                'start_date': issue.start_date,
                'due_date': issue.due_date,
                'created': issue.created,
                'updated': issue.updated,
                'time_spent': issue.time_spent,
                'components': issue.components,
                'labels': issue.labels,
                child_key: {}
            }
        issue_map[issue.key] = hierarchy[issue.key]
