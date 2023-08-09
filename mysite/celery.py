import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# 'celery'프로그램을 위해 DJANGO_SETTINGS_MODULE 변수를 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mysite.settings')
# 'mysite' 라는 애플리케이션 인스턴스를 생성
app = Celery('mysite')
# config_from_object() 메서드는 프로젝트 설정에서 사용자 정의 구성을 로드한다.
# namespace 속성은 settings.py 파일에서 Celery 관련 설정에 포함될 접두사를 지정
# 모든 Celery 설정은 이름에 CELERY_접두사를 포함해야한다. ( ex. CELERY_BROKER_URL )
app.config_from_object('django.conf:settings',namespace='SELERY')
# Celery에게 애플리케이션의 각 애플리케이션 디렉토리의 tasks.py 파일을 찾아 비동기 작업을 자동으로 검색하도록 지시
# Celery는 INSTALLED_APPS에 추가된 각 앱 디렉토리에서 tasks.py 파일을 찾아 그 안에 정의된 비동기 작업을 로드
app.autodiscover_tasks()
