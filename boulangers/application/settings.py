# application/settings.py

from pydantic import BaseSettings


class Settings(BaseSettings):
    jira_domain: str
    jira_email: str
    jira_api_token: str
    jira_epic_field: str = '"Epic Link"'

    class Config:
        env_file = ".env"
