# -*- coding: utf-8 -*-
# @Time        : 2024/9/8
# @Author      : liuboyuan
# @Description :
import requests
import markdown
import imgkit
from datetime import datetime
from typing import Dict, Optional

from framework.inori_plugin_manager.base_plugin import BasePlugin


class GithubDataFetcher(BasePlugin):
    name = "GithubDataFetcher"

    def __init__(self) -> None:
        self.api_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        self.query_params: Optional[Dict[str, str]] = None
        self.token: Optional[str] = None
        self.output_dir = None

    def configure(self, token: str, output_dir=None) -> None:
        """
        配置函数，用于设置GitHub用户token和其他必要的配置
        :param token: GitHub个人访问令牌
        """
        self.token = token
        self.headers["Authorization"] = f"token {self.token}"
        if output_dir:
            self.output_dir = output_dir

    def set_query_params(self, params: Dict[str, str]) -> None:
        """
        设置查询参数
        :param params: 字典类型的查询参数
        """
        self.query_params = params

    def run(self, *args, **kwargs) -> Optional[str]:
        """
        实现GitHub API的数据抓取逻辑，并生成报告文件
        :param output_dir: 保存报告的目录路径，如果未指定，则保存在当前目录
        :param args: 可变参数
        :param kwargs: 关键字参数
        :return: 返回生成的报告文件路径
        """
        import requests

        # 确保查询参数已设置
        if not self.query_params:
            raise ValueError("查询参数未设置，请使用 set_query_params() 方法设置参数")

        # 构建完整的API请求URL
        url = f"{self.api_url}/search/repositories"

        try:
            # 发送GET请求到GitHub API，获取热门项目数据
            response = requests.get(url, headers=self.headers, params=self.query_params)

            # 检查请求是否成功
            if response.status_code == 200:
                # 获取第一个仓库的数据
                repo_data = response.json().get("items", [])[0]

                # 生成报告并保存为文件
                report_file_path = self.generate_report(repo_data, self.output_dir)

                # 返回报告文件的路径
                return report_file_path
            else:
                # 如果请求失败，抛出异常
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            # 处理请求异常
            print(f"请求GitHub API时出错: {e}")
            return None

            # 将报告转换为图片
            # self.convert_markdown_to_image(report, "report.png")
            # print("报告图片已生成并保存为report.png")

    def generate_report(self, repo_data: Dict, output_dir: Optional[str] = None) -> str:
        """
        根据GitHub项目数据生成markdown格式的报告，并保存为文件
        :param repo_data: GitHub仓库的数据
        :param output_dir: 保存报告的目录路径，如果未指定，则保存在当前目录
        :return: 返回markdown格式的报告
        """
        repo_name = repo_data.get("name", "N/A")
        owner = repo_data.get("owner", {}).get("login", "N/A")
        stars = repo_data.get("stargazers_count", "N/A")
        forks = repo_data.get("forks_count", "N/A")
        description = repo_data.get("description", "N/A")
        url = repo_data.get("html_url", "N/A")
        updated_at = repo_data.get("updated_at", "N/A")

        report = f"""
    # GitHub Repository Report: {repo_name}

    **Owner:** {owner}  
    **Stars:** {stars}  
    **Forks:** {forks}  
    **Description:** {description}  
    **URL:** [Link to repository]({url})  
    **Last Updated:** {updated_at}

    Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
        # 生成Markdown文件
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{repo_name}-{timestamp}.md"

        # 如果指定了路径，则将文件保存在该路径下
        if output_dir:
            output_path = f"{output_dir}/{filename}"
        else:
            output_path = filename

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(report)
        print(f"Markdown报告已保存为 {output_path}")

        return output_path

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
    fetcher.set_query_params({"q": "repo:langchain-ai/langchain"})

    fetcher.run()



