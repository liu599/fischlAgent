# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
import markdown
import imgkit
from typing import Optional

from api.plugins.agent.github_client import GitHubClient
from framework.inori_plugin_manager.base_plugin import BasePlugin


class GithubDataFetcher(BasePlugin):
    name = "GithubDataFetcher"

    def __init__(self) -> None:
        self.api_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        self.query_params: Optional[str] = None
        self.token: Optional[str] = None
        self.output_dir = None
        self.github_client: GitHubClient = None
        self.days = 0

    def configure(self, token: str, output_dir=None, days=0) -> None:
        """
        配置函数，用于设置GitHub用户token和其他必要的配置
        :param token: GitHub个人访问令牌
        """
        self.token = token
        self.days = days
        self.headers["Authorization"] = f"token {self.token}"
        self.github_client: GitHubClient = GitHubClient(api_url=self.api_url, headers=self.headers)
        if output_dir:
            self.output_dir = output_dir

    def set_query_params(self, params: str) -> None:
        """
        设置查询参数
        :param params: 字典类型的查询参数
        """
        self.query_params = params

    def run(self, *args, **kwargs) -> (Optional[str], Optional[dict]):
        """
        实现GitHub API的数据抓取逻辑，并生成报告文件
        :param args: 可变参数
        :param kwargs: 关键字参数
        :return: 返回生成的报告文件路径
        """
        if not self.query_params:
            raise ValueError("查询参数未设置，请使用 set_query_params() 方法设置参数")

        report_file_path, updates = self.generate_report(self.query_params, self.output_dir, self.days)
        return report_file_path, updates
        # 将报告转换为图片
        # self.convert_markdown_to_image(report, "report.png")
        # print("报告图片已生成并保存为report.png")

    def generate_report(self, query: str, output_dir: Optional[str] = None, days: Optional[int] = 0) -> (str, dict):
        """
        根据GitHub项目数据生成markdown格式的报告，并保存为文件
        :param repo_data: GitHub仓库的数据
        :param output_dir: 保存报告的目录路径，如果未指定，则保存在当前目录
        :return: 返回markdown格式的报告
        """
        print(days)
        if days != 0:
            report, updates = self.github_client.export_progress_by_date_range(query, days, output_dir=output_dir)
        else:
            report, updates = self.github_client.export_daily_progress(query, output_dir=output_dir)
        return report, updates

    def convert_markdown_to_image(self, markdown_text: str, output_file: str) -> None:
        """
        将markdown格式的报告转换为图片
        :param markdown_text: markdown格式的文本
        :param output_file: 保存图片的文件名
        """
        html = markdown.markdown(markdown_text)
        config = imgkit.config(wkhtmltoimage='C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe')  # 修改为你的路径
        imgkit.from_string(html, output_file, config=config)


# 示例运行脚本
if __name__ == "__main__":
    fetcher = GithubDataFetcher()
    token = input("GitHub API token: ")
    fetcher.configure(token, output_dir=None)  # 替换为你的GitHub Token

    # 设置查询参数
    fetcher.set_query_params("repo:langchain-ai/langchain")

    fetcher.run()



