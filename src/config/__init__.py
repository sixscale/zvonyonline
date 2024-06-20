import pymysql
from .celery import app as zvonyonline_celery_app

pymysql.install_as_MySQLdb()

__all__ = ('zvonyonline_celery_app',)
