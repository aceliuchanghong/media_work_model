import config
from core.action.base_crawler import BaseCrawler
import json
import os


class Crawler(BaseCrawler):
    def _extract_last_part(self, url):
        # 去除URL末尾的"/"（如果存在）
        if url.endswith('/'):
            url = url[:-1]

        # 分割URL并提取最后一部分
        parts = url.rsplit('/', 1)
        return parts[-1]

    def work(self, url, user):
        """
        爬取对于url,获取数据文件保存到{user}目录下存为{user}_output.txt
        """
        # 获取数据
        response = self._get(url)
        if response is None:
            self.logger.error(f"Failed to get data from {url}")
            return
        path = self._extract_last_part(url)
        user_dir = os.path.join(os.getcwd(), user)
        user_dir = os.path.join(user_dir, path)
        self._validate_output_path(user_dir)

        # 保存数据到文件
        output_file = os.path.join(user_dir, f"{user}_output.txt")
        output2_file = os.path.join(user_dir, f"{user}_output2.txt")
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(response.get("text"), file, indent=4, ensure_ascii=False)
        with open(output2_file, 'w', encoding='utf-8') as file2:
            json.dump(response.get("images"), file2, indent=4, ensure_ascii=False)

        self.logger.info(f"Data successfully saved to {output_file}")
        self.logger.info(f"Data successfully saved to {output2_file}")


if __name__ == '__main__':
    cl = Crawler(config)
    cl.work('https://mp.weixin.qq.com/s/7m3lVegUOigG1Uy904GmaA', 'liu')
    cl.work('https://www.sohu.com/a/744144846_121687421', 'liu')
