# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
import requests
from typing import Dict, List


class GitHubClient:
    def __init__(self, api_url: str = "https://api.github.com", headers: Dict[str, str] = None):
        self.api_url = api_url
        self.headers = headers or {"Accept": "application/vnd.github.v3+json"}

    def search_repositories(self, query: str) -> Dict:
        """
        搜索 GitHub 仓库
        :param query: 搜索查询字符串
        :return: 返回搜索结果的 JSON 数据
        """
        url = f"{self.api_url}/search/repositories"
        response = requests.get(url, headers=self.headers, params={"q": query})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Unable to fetch repositories: {response.status_code} {response.text}")


    def get_issues(self, repo_name: str, owner: str) -> str:
        url = f"{self.api_url}/repos/{owner}/{repo_name}/issues"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            issues = response.json()
            return "\n".join(f"- {issue.get('title')} (#{issue.get('number')})" for issue in issues)
        else:
            return "Unable to fetch issues."

    def get_commits(self, repo_name: str, owner: str) -> str:
        url = f"{self.api_url}/repos/{owner}/{repo_name}/commits"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            commits = response.json()
            return "\n".join(
                f"- {commit.get('commit', {}).get('message')} (by {commit.get('commit', {}).get('author', {}).get('name')})"
                for commit in commits)
        else:
            return "Unable to fetch commits."

    def get_pull_requests(self, repo_name: str, owner: str) -> str:
        url = f"{self.api_url}/repos/{owner}/{repo_name}/pulls"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            pulls = response.json()
            return "\n".join(f"- {pull.get('title')} (#{pull.get('number')})" for pull in pulls)
        else:
            return "Unable to fetch pull requests."
