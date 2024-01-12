from abc import abstractmethod
from functools import lru_cache
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from core.worker import Worker


class BaseCrawler(Worker):

    def __init__(self, config):
        super().__init__(config)
        self.session = self._create_session()
        self.content_regex = re.compile(r'/content/|/uploads/|/media/')

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

    def _get2(self, url, content_selector='article, .post, .content, body',
              exclude_selectors=None):
        """
        Use playwright to send GET requests and extract main content from the page.
        """
        if exclude_selectors is None:
            exclude_selectors = ['script', 'style', 'header', 'footer', 'nav', 'aside', 'toolbarBox']
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")

            try:
                # Wait for the content selector to be available
                page.wait_for_selector(content_selector, timeout=4000)
                # Extract the HTML content
                html_content = page.query_selector(content_selector).inner_html()
                # print(html_content)

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

    def fetch_html_content(self, url, content_selector='article, .post, .content, body'):
        """
        Use playwright to send GET requests and return the HTML content of the page.
        """
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

        with sync_playwright() as p:
            browser = p.chromium.launch()
            # Create a new browser context with the specified user agent
            context = browser.new_context(user_agent=user_agent)

            page = context.new_page()
            try:
                response = page.goto(url, wait_until="domcontentloaded")
                # Check if the page was loaded successfully
                if response.ok:
                    # Wait for the content selector to be available
                    page.wait_for_selector(content_selector, timeout=4000)
                    # Extract the HTML content
                    html_content = page.query_selector(content_selector).inner_html()
                    return html_content
                else:
                    print(f"Page load failed with status: {response.status}")
                    return None
            except Exception as e:
                print(f"Error occurred: {e}")
                return 'None'
            finally:
                # Ensure the browser is closed even if an error occurs
                context.close()
                browser.close()

    def parse_html_content2(self, html_content, exclude_selectors=None):
        """
        Parse the HTML content and extract main content as text.
        """
        if exclude_selectors is None:
            exclude_selectors = ['script', 'style', 'header', 'footer', 'nav', 'aside', 'toolbarBox']

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
        return content

    def parse_html_content(self, html_content, exclude_selectors=None):
        """
        Parse the HTML content and extract main content as text and images.
        """
        if exclude_selectors is None:
            exclude_selectors = ['script', 'style', 'header', 'footer', 'nav', 'aside', 'toolbarBox']

        # Use BeautifulSoup to parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove unwanted tags
        for selector in exclude_selectors:
            for element in soup.select(selector):
                element.extract()

        # Extract text
        text = soup.get_text()

        # Clean text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Extract images
        images = self.extract_images(soup)

        # Combine text and images
        content = {'text': text, 'images': images}
        return content

    @lru_cache(maxsize=1024)
    def is_relevant_image(self, src, alt, img):
        """
        Heuristic to determine if an image is relevant to the content.
        """
        # Check if the image source contains certain keywords
        if self.content_regex.search(src):
            return True

        # Check if the alt text is sufficiently descriptive
        if len(alt) > 10:  # arbitrary length threshold
            return True

        # Check if the image is within certain HTML tags that likely contain main content
        for parent in img.parents:
            if parent.name in ['article', 'main', 'section']:
                return True

        return False

    def extract_images(self, soup):
        """
        Extract images from the BeautifulSoup object, applying heuristic filters.
        """
        images = []
        for img in soup.select('img[src]'):  # Only select img tags with src attribute
            src = img['src']
            alt = img.get('alt', '')

            # Apply heuristic filters
            if self.is_relevant_image(src, alt, img):
                images.append(src)

        return images

    def _get(self, url):
        content = self.fetch_html_content(url)
        ans = self.parse_html_content(content)
        return content, ans

    @abstractmethod
    def work(self, *args, **kwargs):
        """
        执行爬取任务。这个方法应该被所有爬虫子类实现。
        """
        pass
