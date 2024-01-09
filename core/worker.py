import logging
from abc import ABC, abstractmethod
import os


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

    def _validate_output_path(self, output_path):
        """
        Validate the output path. If the path is a directory, create it if it doesn't exist.
        If it's a file path and the directory does not exist, create it.
        """
        if os.path.isdir(output_path) or not os.path.splitext(output_path)[1]:
            output_dir = output_path
        else:
            output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_path

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
