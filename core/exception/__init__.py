# exception/__init__.py

class MediaWorkModelException(Exception):
    """基础异常类，所有自定义异常都继承自这个类"""
    pass


class CrawlerException(MediaWorkModelException):
    """爬虫相关异常"""
    pass


class ProcessorException(MediaWorkModelException):
    """处理器相关异常"""
    pass


class UploaderException(MediaWorkModelException):
    """上传相关异常"""
    pass


# 爬虫异常
class CrawlerLoginException(CrawlerException):
    """爬虫登录异常"""
    pass


class CrawlerFetchException(CrawlerException):
    """爬虫获取数据异常"""
    pass


# 处理器异常
class ProcessorInvalidFormatException(ProcessorException):
    """处理器无效格式异常"""
    pass


class ProcessorExecutionException(ProcessorException):
    """处理器执行异常"""
    pass


# 上传异常
class UploaderLoginException(UploaderException):
    """上传登录异常"""
    pass


class UploaderPublishException(UploaderException):
    """上传发布异常"""
    pass
