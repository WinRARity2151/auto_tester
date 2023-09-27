from logging.handlers import RotatingFileHandler
import logging
from selenium import webdriver


class BasePage:
    driver = webdriver.Chrome()

    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(
        "app.log", maxBytes=1024 * 1024, backupCount=10, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    LOGGER.addHandler(file_handler)

    @classmethod
    def logger(cls, custom_text):
        def decorator(func):
            def wrapper(*args, **kwargs):
                cls.LOGGER.info(custom_text)
                try:
                    result = func(*args, **kwargs)
                    cls.LOGGER.info("Выполнено")
                    return result
                except Exception as e:
                    cls.LOGGER.error(e)
                    raise SystemExit(1)

            return wrapper

        return decorator
