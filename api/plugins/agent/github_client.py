# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
import textwrap

import requests
from typing import Dict, List
from datetime import datetime, date, timedelta


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

    def get_issues(self, repo_name: str, owner: str, since=None, until=None) -> str:
        url = f"{self.api_url}/repos/{owner}/{repo_name}/issues"
        params = {
            'state': 'closed',  # 仅获取已关闭的问题
            'since': since,
            'until': until
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        if response.status_code == 200:
            issues = response.json()
            return "\n".join(f"- {issue.get('title')} (#{issue.get('number')})" for issue in issues)
        else:
            return "Unable to fetch issues."

    def get_commits(self, repo_name: str, owner: str, since=None, until=None) -> str:
        url = f"{self.api_url}/repos/{owner}/{repo_name}/commits"
        params = {}
        if since:
            params['since'] = since  # 如果指定了开始日期，添加到参数中
        if until:
            params['until'] = until  # 如果指定了结束日期，添加到参数中
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        if response.status_code == 200:
            commits = response.json()
            return "\n".join(
                f"- {commit.get('commit', {}).get('message')} (by {commit.get('commit', {}).get('author', {}).get('name')})"
                for commit in commits)
        else:
            return "Unable to fetch commits."

    def get_pull_requests(self, repo_name: str, owner: str, since=None, until=None) -> str:
        url = f"{self.api_url}/repos/{owner}/{repo_name}/pulls"
        params = {
            'state': 'closed',  # 仅获取已合并的拉取请求
            'since': since,
            'until': until
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        if response.status_code == 200:
            pulls = response.json()
            return "\n".join(f"- {pull.get('title')} (#{pull.get('number')})" for pull in pulls)
        else:
            return "Unable to fetch pull requests."

    def fetch_updates(self, query: str, since=None, until=None) -> Dict:
        # 获取指定仓库的更新，可以指定开始和结束日期
        repos = self.search_repositories(query)
        repo_data = None
        if "items" in repos and len(repos["items"]) > 0:
            repo_data = repos["items"][0]
        if repo_data is None:
            raise Exception("Github API Failure")
        repo_name = repo_data.get("name", "UnknownRepo")
        owner = repo_data.get("owner", {}).get("login", "N/A")
        updates = {
            'info': {
                "owner": owner,
                "repo": repo_name,
                "stars": repo_data.get("stargazers_count", "NA"),
                "forks": repo_data.get("forks_count", "NA"),
                "description": repo_data.get("description", "NA"),
                "url": repo_data.get("html_url", "NA"),
                "updated_at": repo_data.get("updated_at", "NA"),
                "from": since if since is not None else None,
                "to": until if until is not None else None,
                "days": 0,
            },
            'commits': self.get_commits(repo_name, owner, since, until),  # 获取提交记录
            'issues': self.get_issues(repo_name, owner, since, until),  # 获取问题
            'pull_requests': self.get_pull_requests(repo_name, owner, since, until)  # 获取拉取请求
        }
        return updates

    def format_report(self, updates: Dict) -> str:
        if updates['info']['from'] is None:
            tr = "No special range"
            tr_type = "Custom"
        elif updates['info']['to'] is None:
            tr = f"{updates['info']['from']}"
            tr_type = "Daily Report"
        else:
            tr = f"{updates['info']['from']} - {updates['info']['to']}"
            tr_type = f"{updates['info']['days']} days report"
        report = f"""\
# GitHub Repository Report
- **Repo Name:** {updates["info"]["repo"]}
- **Type:** {tr_type}
- **Time Range:** {tr}
- **Owner:** {updates["info"]["owner"]}
- **Stars:** {updates["info"]["stars"]}
- **Forks:** {updates["info"]["forks"]}
- **Description:** {updates["info"]["description"]}
- **URL:** [Link to repository]({updates["info"]["url"]})
- **Last Updated:** {updates["info"]["updated_at"]}
## Issues
{updates["issues"]}
## Commits
{updates["commits"]}
## Pull Requests
{updates["pull_requests"]}

------
Created by Github Agent
Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\
        """
        return textwrap.dedent(report)

    def export_report(self, repo_name, report, output_dir=None) -> str:
        # 生成Markdown文件
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{repo_name}-{timestamp}.md"
        # 如果指定了路径，则将文件保存在该路径下
        if output_dir is not None:
            output_path = f"{output_dir}/{filename}"
        else:
            output_path = filename
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(report)

        print(f"Markdown报告已保存为 {output_path}")
        return output_path

    def export_daily_progress(self, query, output_dir=None) -> str:
        today = datetime.now().date().isoformat()  # 获取今天的日期
        # today = date.today()
        # since = today - timedelta(days=1)
        # since = since.isoformat()
        updates = self.fetch_updates(query, since=today)  # 获取今天的更新数据
        repo_name = updates["info"]["repo"]
        report = self.format_report(updates)
        return self.export_report(repo_name, report, output_dir)

    def export_progress_by_date_range(self, query, days, output_dir=None) -> str:
        today = date.today()  # 获取当前日期
        since = today - timedelta(days=days)  # 计算开始日期
        updates = self.fetch_updates(query, since=since.isoformat(), until=today.isoformat())  # 获取指定日期范围内的更新
        repo_name = updates["info"]["repo"]
        updates["info"]["days"] = days
        report = self.format_report(updates)
        return self.export_report(repo_name, report, output_dir)


if __name__ == "__main__":
    today = datetime.now().date().isoformat()
    print(today)
