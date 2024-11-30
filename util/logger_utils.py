import logging
import os


def configure_logger(name: str, log_file=None, log_level=logging.INFO):
    """配置日志器"""
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 如果指定了日志文件路径，添加文件处理器
    if log_file:
        if not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # 添加控制台处理器
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


def log_info(logger: logging.Logger, message: str):
    """
    调用说明:采用(模块名.log_info)的方法进行调用,切勿用(对象名.log_info)进行调用
    记录INFO级别日志"""
    logger.info(message)


def log_warning(logger: logging.Logger, message: str):
    """
    调用说明:采用(模块名.log_info)的方法进行调用,切勿用(对象名.log_info)进行调用
    记录WARNING级别日志"""
    logger.warning(message)


def log_error(logger: logging.Logger, message: str):
    """
    调用说明:采用(模块名.log_info)的方法进行调用,切勿用(对象名.log_info)进行调用
    记录ERROR级别日志"""
    logger.error(message)
