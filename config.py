# -*- coding: utf-8 -*-
import os
import multiprocessing

"""
部分配置从环境变量从环境变量中导入并提供了一个默认值
"""

"""
logging 的使用:https://blog.csdn.net/afterlake/article/details/104367697
日志级别: CRITICAL> ERROR> WARNING > INFO > DEBUG > NOTSET 
"""

MODE = 'develop'  # develop: 开发模式(无log日志记录); production: 生产模式

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secrete key'
    # 设置接口返回中文
    JSON_AS_ASCII = False
    #Api docs
    RESTFUL_API_DOC_EXCLUDE = []

    # SQLAlchemy commit方式
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    """
    生产配置
    """
    BIND = '127.0.0.1:5000'
    WORKERS = multiprocessing.cpu_count() * 2 + 1
    WORKER_CONNECTIONS = 10000
    BACKLOG = 64
    TIMEOUT = 60
    LOG_LEVEL = 'INFO'
    LOG_DIR_PATH = os.path.join(basedir, 'logs')
    LOG_FILE_MAX_BYTES = 1024 * 1024 * 100
    LOG_FILE_BACKUP_COUNT = 10
    PID_FILE = 'run.pid'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Api Docs
    # disable api docs
    API_DOC_ENABLE = False

    # 配置日志
    LOGGER_CONF = {
        'version': 1,
        'formatters': {'default': {
            'format': '%(asctime)s[%(name)s][%(levelname)s] :%(levelno)s: %(message)s',
        }},
        'handlers': {'info_handler': {
            'class': 'logging.handlers.RotatingFileHandler',  # 输出到文件
            'level': 'INFO',
            'formatter': 'default',
            'filename': './logs/info.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 20,  # most 20 extensions
            'encoding': 'utf8',
        }, 'error_handler': {
            'class': 'logging.handlers.RotatingFileHandler',  # 输出到文件
            'level': 'ERROR',
            'formatter': 'default',
            'filename': './logs/info.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 20,  # most 20 extensions
            'encoding': 'utf8'
        }},
        'root': {
            # 'level': 'INFO',
            'handlers': ['info_handler']
        }
    }


class DevelopConfig(Config):
    """
    开发配置
    """
    BIND = '0.0.0.0:5000'
    WORKERS = 2
    WORKER_CONNECTIONS = 1000
    BACKLOG = 64
    TIMEOUT = 30
    LOG_LEVEL = 'DEBUG'
    LOG_DIR_PATH = os.path.join(basedir, 'logs')
    LOG_FILE_MAX_BYTES = 1024 * 1024
    LOG_FILE_BACKUP_COUNT = 1
    PID_FILE = 'run.pid'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置日志
    LOGGER_CONF = {
        'version': 1,
        'formatters': {'default': {
            'format': '%(asctime)s[%(name)s][%(levelname)s] :%(levelno)s: %(message)s',
        }},
        'handlers': {'console': {
            'class': 'logging.StreamHandler',  # 输出到控制台
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://flask.logging.wsgi_errors_stream'  # 监听flask日志
        }},
        'root': {
            # 'level': 'INFO',
            'handlers': ['console']
        }
    }


if MODE == 'production':
    config = ProductionConfig
else:
    config = DevelopConfig


