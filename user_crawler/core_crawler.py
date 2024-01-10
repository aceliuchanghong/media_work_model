import config
from core.action.base_crawler import BaseCrawler
import json
import os


class Crawler(BaseCrawler):
    def work(self, url, user):
        """
        爬取对于url,获取数据文件保存到{user}目录下存为{user}_output.json
        """
        # 获取数据
        response = self._get(url)
        if response is None:
            self.logger.error(f"Failed to get data from {url}")
            return
        print(response)

        user_dir = os.path.join(os.getcwd(), user)
        self._validate_output_path(user_dir)

        # 保存JSON数据到文件
        output_file = os.path.join(user_dir, f"{user}_output.json")
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(response, file, indent=4, ensure_ascii=False)

        self.logger.info(f"Data successfully saved to {output_file}")


if __name__ == '__main__':
    cl = Crawler(config)
    cl.work('https://mp.weixin.qq.com/s/7m3lVegUOigG1Uy904GmaA', 'liu')
    cl.work('https://www.sohu.com/a/744144846_121687421', 'liu')
