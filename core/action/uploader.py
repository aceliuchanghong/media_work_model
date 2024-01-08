from abc import abstractmethod
from core.worker import Worker


class Uploader(Worker):
    def __init__(self, config):
        super().__init__(config)
        # 初始化任何需要的属性，例如认证信息

    def _upload_file(self, platform_client, file_path, metadata):
        """
        使用指定平台的客户端上传文件。
        """
        try:
            # 这里假设平台客户端有一个upload方法
            response = platform_client.upload(file_path, metadata)
            return response
        except Exception as e:
            self.logger.error(f"Upload failed: {e}")
            return None

    def _process_response(self, response):
        """
        处理上传后的响应。
        """
        if response:
            # 根据响应内容进行处理，例如解析上传结果
            self.logger.info("Upload successful.")
        else:
            self.logger.error("Upload failed, no response.")

    @abstractmethod
    def work(self, file_path, metadata, platform_client):
        """
        上传文件到指定平台。这个方法应该被所有上传子类实现。
        """
        # 调用上传方法
        response = self._upload_file(platform_client, file_path, metadata)
        # 处理响应
        self._process_response(response)
