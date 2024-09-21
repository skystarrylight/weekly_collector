# infrastructure/jira_client.py

import aiohttp
from aiohttp import BasicAuth
from typing import List
from boulangers.domain.issue import Issue
from boulangers.application.ports import IssueRepositoryPort
from datetime import datetime

class JiraClient(IssueRepositoryPort):
    def __init__(self, domain: str, email: str, api_token: str, epic_field: str = '"Epic Link"'):
        self.base_url = f'https://{domain}.atlassian.net/rest/api/3'
        self.auth = BasicAuth(email, api_token)
        self.epic_field = epic_field

    async def fetch_issues(self, jql_query: str) -> List[Issue]:
        search_url = f'{self.base_url}/search'
        params = {'jql': jql_query, 'maxResults': 1000}  # 최대 1000개 이슈 가져오기
        async with aiohttp.ClientSession(auth=self.auth) as session:
            async with session.get(search_url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                issues_data = data.get('issues', [])
                return [self._parse_issue(issue_data) for issue_data in issues_data]

    @staticmethod
    def _parse_issue(issue_data) -> Issue:
        """
        주어진 issue_data에서 필드를 파싱하여 Issue 객체를 생성합니다.
        None 타입이 들어올 수 있는 모든 필드를 안전하게 처리합니다.
        """
        # fields와 그 하위 필드를 안전하게 파싱
        print(issue_data)
        fields = issue_data.get('fields', {})
        issue_type_info = fields.get('issuetype', {}) or {}
        status_info = fields.get('status', {}) or {}
        assignee_info = fields.get('assignee', {}) or {}

        # 안전하게 필드 값들을 추출 (None일 경우 기본값 설정)
        key = issue_data.get('key', '')  # 'key'가 없으면 빈 문자열로 설정
        summary = fields.get('summary', '')  # 요약 정보
        description_info = fields.get('description', {}) or {}
        description = JiraClient._parse_description(description_info)  # description 필드가 중첩된 구조이므로 별도 처리

        # 상태와 담당자 정보 추출
        status = status_info.get('name', '')  # 상태 정보가 없으면 빈 문자열로 설정
        assignee = assignee_info.get('displayName', 'Unassigned')  # 담당자 정보가 없으면 'Unassigned'로 설정

        # 이슈 타입 처리 (에픽일 경우에도 안전하게 처리)
        issue_type = issue_type_info.get('name', 'Issue')  # 이슈 타입이 없으면 'Issue'로 설정

        # 시작일과 종료일 파싱
        start_date_str = fields.get('customfield_10015', None)  # custom 필드에 시작일 정보가 있을 수 있음
        due_date_str = fields.get('duedate', None)  # 종료일

        # 날짜를 안전하게 파싱
        start_date = JiraClient._parse_date(start_date_str)
        due_date = JiraClient._parse_date(due_date_str)

        return Issue(
            key=key,
            summary=summary,
            description=description,
            status=status,
            assignee=assignee,
            type=issue_type,
            start_date=start_date,
            due_date=due_date
        )

    @staticmethod
    def _parse_description(description_info):
        """
        중첩된 description 필드를 안전하게 파싱.
        content 리스트에서 각 텍스트를 추출하여 하나의 문자열로 반환.
        """
        if not description_info or not isinstance(description_info, dict):
            return ''

        # description이 중첩된 구조를 가짐
        content_list = description_info.get('content', [])
        if not content_list:
            return ''

        description_text = ''
        for content in content_list:
            # content 안에서 텍스트 추출
            if 'content' in content:
                paragraph_content = content['content']
                for paragraph in paragraph_content:
                    text = paragraph.get('text', '')
                    description_text += text + ' '

        return description_text.strip()

    @staticmethod
    def _parse_date(date_str):
        """
        날짜 문자열을 안전하게 파싱. 형식이 맞지 않거나 None일 경우 None 반환.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        except (ValueError, TypeError):
            return None
