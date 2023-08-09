# Django가 시작될때 Celery 모듈을 로드하기 위해 추가
from .celery import app as celery_app

__all__ = ['celery_app']