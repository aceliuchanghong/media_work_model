from abc import abstractmethod
import requests
from core.worker import Worker
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


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
        session.headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
        if self.config.PROXY:
            session.proxies.update(self.config.PROXY)
        return session

    def _get(self, url, content_selector='article, .post, .content, body',
             exclude_selectors=None):
        """
        Use playwright to send GET requests and extract main content from the page.
        """
        if exclude_selectors is None:
            exclude_selectors = ['script', 'style', 'header', 'footer', 'nav', 'aside', 'toolbarBox']
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)

            try:
                # Wait for the content selector to be available
                page.wait_for_selector(content_selector, timeout=4000)
                # Extract the HTML content
                html_content = page.query_selector(content_selector).inner_html()

                # Use BeautifulSoup to parse HTML
                soup = BeautifulSoup(html_content, 'html.parser')

                # Remove unwanted tags
                for selector in exclude_selectors:
                    for element in soup.select(selector):
                        element.extract()

                # Get text
                text = soup.get_text()

                # Clean text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)

                # Combine text
                content = {'text': text}

                browser.close()
                return content
            except Exception as e:
                self.logger.error(f"Error occurred: {e}")
                browser.close()
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
