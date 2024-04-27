import logging
import os.path
import sys
from loguru import logger
from datetime import datetime

loglevel_mapping = {
    50: 'CRITICAL',
    40: 'ERROR',
    30: 'WARNING',
    20: 'INFO',
    10: 'DEBUG',
    0: 'NOTSET',
}


class InterceptHandler(logging.Handler):

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class MyInterceptor(logging.Handler):

    def handle(self, record):
        # 修改日志级别
        record.level = logging.WARNING

        # 添加自定义元数据
        # record.extra['my_custom_metadata'] = 'hello, world!'

        # 继续记录日志
        super().handle(record)

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class CustomizeLogger:
    __mqtt_client = None

    @classmethod
    def make_logger(cls, config):
        filename = config['filename']
        file_path = config['path']

        # Get current date and time
        now = datetime.now()
        # Format date and time
        timestamp = now.strftime("%Y%m%d_%H%M")
        # Use the timestamp as the filename
        formated_filename = f"{filename}_{timestamp}.log"

        abs_filepath = os.path.join(os.getcwd(), file_path)
        logger = cls.customize_logging(
            # config['path'),
            filepath=os.path.join(abs_filepath, formated_filename),
            level=config['level'],
            retention=config['retention'],
            rotation=config['rotation'],
            format=config['format']
        )
        return logger

    @classmethod
    def customize_logging(cls,
                          filepath: str,
                          level: str,
                          rotation: str,
                          retention: str,
                          format: str
                          ):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        logger.add(
            filepath,
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        # logger.add(
        #     cls.__mqtt_sink,
        #     enqueue=True,
        #     backtrace=True,
        #     level=level.upper(),
        #     format=format
        # )

        logging.basicConfig(handlers=[InterceptHandler(), MyInterceptor()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    # @classmethod
    # def set_mqtt_client(cls, mqtt_client):
    #     cls.__mqtt_client = mqtt_client
    #
    # @classmethod
    # def __mqtt_sink(cls, message):
    #     if cls.__mqtt_client is None:
    #         time.sleep(1)
    #         return
    #     cls.__mqtt_client.publish(Topic.FLOWCHART_STATUS.value, message)
