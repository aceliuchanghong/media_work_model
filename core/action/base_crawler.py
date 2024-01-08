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
