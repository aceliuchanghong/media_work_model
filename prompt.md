我需要一个工程,帮我部署到服务器,完成每日任务,所以我需要设计一下项目结构 以下是当前大致的结构
我的要做的工作是1.先去某网站爬取需要的文件存到某处 2.视频处理好后生成新的视频 3.视频上传到不同平台
```
media_work_model/
|
├── main.py
├── requirements.txt
├── config/
│   ├── __init__.py
│   └── base_config.py
├── core/
│   ├── __init__.py
│   ├── worker.py
│   ├── action/
│   │   ├── __init__.py
│   │   ├── base_crawler.py
│   │   ├── processor.py
│   │   └── uploader.py
│   ├── exception/
│   │   └── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── bilibili.py
│   │   └── xiaohongshu.py
│   └── proxy/
│       ├── __init__.py
│       ├── proxy_account_pool.py
│       ├── proxy_ip_pool.py
│       └── proxy_ip_provider.py
├── docs/
│   ├── README_EN.md
│   └── static/
│       └── imgs/
├── logs/
│   └── __init__.py
├── media_platform/
│   ├── __init__.py
│   ├── bilibili/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── core.py
│   │   ├── exception.py
│   │   ├── field.py
│   │   ├── help.py
│   │   └── login.py
│   └── xhs/
│       ├── __init__.py
│       ├── client.py
│       ├── core.py
│       ├── exception.py
│       ├── field.py
│       ├── help.py
│       └── login.py
├── test/
│   ├── __init__.py
│   └── testfiles/
└── utils/
    ├── __init__.py
    └── time_util.py
``` 
其中 worker 写法
```
import logging
from abc import ABC, abstractmethod
class Worker(ABC):
    def __init__(self, config):
        """
        初始化Worker类
        """
        self.config = config
        self.logger = self._setup_logger()
    def _setup_logger(self):
        """
        设置日志记录器
        """
        logger = logging.getLogger(self.__class__.__name__)
        # 可以根据需要配置日志记录器，比如设置日志级别、格式和输出位置
        logger.setLevel(self.config.LOG_LEVEL)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    @abstractmethod
    def work(self, *args, **kwargs):
        """
        处理媒体文件。这个方法应该被所有子类实现。
        具体的参数可以根据处理任务的不同而变化。
        """
        pass
    def run(self, *args, **kwargs):
        """
        运行工作流程
        """
        try:
            self.work(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            # 这里可以添加错误处理逻辑，比如重试或发送通知
            raise
```
其中 base_crawler 写法
```
from abc import abstractmethod
import requests
from core.worker import Worker
class BaseCrawler(Worker):
    def __init__(self, config):
        super().__init__(config)
        self.session = self._create_session()
    def _create_session(self):
        """
        创建并配置网络会话
        """
        session = requests.Session()
        # 可以在这里设置代理、头部信息等
        session.headers.update({'User-Agent': 'Your User Agent'})
        if self.config.PROXY:
            session.proxies.update(self.config.PROXY)
        return session
    def _get(self, url, **kwargs):
        """
        发送GET请求
        """
        try:
            response = self.session.get(url, **kwargs)
            response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常
            return response
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTPError occurred: {e}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"RequestException occurred: {e}")
        return None
    def _post(self, url, data=None, json=None, **kwargs):
        """
        发送POST请求
        """
        try:
            response = self.session.post(url, data=data, json=json, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTPError occurred: {e}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"RequestException occurred: {e}")
        return None
    @abstractmethod
    def work(self, *args, **kwargs):
        """
        执行爬取任务。这个方法应该被所有爬虫子类实现。
        """
        pass
```

