# Fischl 小艾米个人助理项目

实验性AI Agent项目

## 项目描述

- 基于GPT4
- 采用前后端分离, 本repo只提供API及内部Agent逻辑, 前端逻辑见[小草神项目](https://github.com/liu599/NahidaSystem)
- GitHub Sentinel is an open-source AI Agent designed for developers and project managers.
- Provides a Flask API for easy integration.
- Automatically subscribes to specific GitHub repositories and tracks the latest updates.
- Generates detailed reports on repository activity.
- Automatically sends notifications to keep users informed of new developments in real time.
- 插件学习自以下项目
  - https://github.com/DjangoPeng/GitHubSentinel
  - https://github.com/DjangoPeng/GitHubSentinel/tree/v0.0.1

## API文档

- `python main.py`
- 启动后访问localhost:5010即可

## 大模型API实验

```
  curl --location 'http://localhost:5010/fischl_api/v1/chat_api' \
  --header 'Content-Type: application/json' \
  --data '{
      "model": "azure",
      "q": "《守护甜心》的作者是谁?"
  }'
  
  
```

返回
```
{
    "code": 20000,
    "data": {
        "message": {
            "content": "《守护甜心》（Shugo Chara!）的作者是PEACH-PIT，这是一个由两位日本女性漫画家组成的团队，成员包括樱井日菜子（日名：桜井 日菜子，Sakurai Hinako）和秋田光彦（日名：秋田 光彦，Akita Mikihiko）。《守护甜心》是他们创作的一部非常受欢迎的少女漫画，讲述了主角日奈森亚梦与她的守护角色们的故事。",
            "metadata": {
                "content_filter_results": {
                    "hate": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "self_harm": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "sexual": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "violence": {
                        "filtered": false,
                        "severity": "safe"
                    }
                },
                "finish_reason": "stop",
                "logprobs": null,
                "model_name": "gpt-4",
                "prompt_filter_results": [
                    {
                        "content_filter_results": {
                            "hate": {
                                "filtered": false,
                                "severity": "safe"
                            },
                            "self_harm": {
                                "filtered": false,
                                "severity": "safe"
                            },
                            "sexual": {
                                "filtered": false,
                                "severity": "safe"
                            },
                            "violence": {
                                "filtered": false,
                                "severity": "safe"
                            }
                        },
                        "prompt_index": 0
                    }
                ],
                "system_fingerprint": "fp_e49e4201a9",
                "token_usage": {
                    "completion_tokens": 171,
                    "prompt_tokens": 22,
                    "total_tokens": 193
                }
            },
            "run_id": "run-ac807686-14d6-47f5-b6c0-46c091301230-0"
        }
    },
    "message": "操作成功"
}
```


