# # -*- coding: UTF-8 -*-
"""
        ╭﹌☆﹌﹌﹌☆﹌╮
       ∣　　　　　　  ∣
      ∣　●　　　●　∣
     ∣　　　▽　　  ∣
    ╰ —————— ╯
     ∣　﹏　﹏　∣
    ╰∪———∪╯

        ┏┛┻━━━┛ ┻┓
       ┃　　　━　　　 ┃
      ┃　┳┛　 ┗┳　┃
     ┃　　　　　　   ┃
    ┃　　　┻　　　 ┃
   ┗━┓　 ┏━━━┛
      ┃　 ┃
     ┃　 ┗━━━━━━━━━ ━┓
    ┃　　　　　　　            ┣┓
   ┃　　　　                  ┏┛
  ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
     ┃ ┫ ┫      ┃ ┫ ┫
    ┗ ┻ ┛      ┗ ┻ ┛

"""


import logging
import logging.config
from flask import Flask, current_app
from config import config



app = Flask(__name__)
# logging.config.dictConfig(logger_conf)


def create_app():
    app = Flask(__name__)
    # 方法一日志设置
    # handler = logging.FileHandler(filename="test.log", encoding='utf-8')
    # handler.setLevel("DEBUG")
    # format_ = "%(asctime)s[%(name)s][%(levelname)s] :%(levelno)s: %(message)s"
    # formatter = logging.Formatter(format_)
    # handler.setFormatter(formatter)
    # app.logger.addHandler(handler)
    # 方法二日志设置
    logger_conf = config.LOGGER_CONF
    logging.config.dictConfig(logger_conf)
    return app


app = create_app()


@app.route("/", methods=["GET"])
def test():
    current_app.logger.info("this is info")
    current_app.logger.debug("this is debug")
    current_app.logger.warning("this is warning")
    current_app.logger.error("this is error")
    current_app.logger.critical("this is critical")
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)