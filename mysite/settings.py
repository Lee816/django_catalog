"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os, json
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

with open(os.path.join(BASE_DIR, "secrets.json")) as f:
    secrets = json.loads(f.read())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["mysite.com", "localhost", "127.0.0.1"]


SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    "account.apps.AccountConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog.apps.BlogConfig",
    "taggit",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.postgres",
    "social_django",
    "django_extensions",
    "images.apps.ImagesConfig",
    'easy_thumbnails',
    'actions.apps.ActionsConfig',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": secrets["DATABASE_NAME"],
        "USER": secrets["DATABASE_USER"],
        "PASSWORD": secrets["DATABASE_PASSWORD"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 이메일 서버 구성
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = secrets["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = secrets["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = "587"
EMAIL_USE_TLS = True
# 이메일을 콘솔로 보여주기
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# 로그인
# 로그인에 성공후 next 매개변수가 요청에 없을때 리디렉션할 url
LOGIN_REDIRECT_URL = "dashboard"
# 로그인하도록 리디렉션할 url
LOGIN_URL = "login"
# 로그아웃 하도록 리디렉션할 url
LOGOUT_URL = "logout"


# 미디어파일
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# 사용자 인증 백엔드
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # 기본 모델 백엔드 사용
    "account.authentication.EmailAuthBackend",  # 사용자 커스텀 인증 백엔드를 포함
    "social_core.backends.facebook.FacebookOAuth2",  # 페이스북 인증
    "social_core.backends.google.GoogleOAuth2",  # 구글 인증
]

# 구글 인증
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = secrets["SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"]
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = secrets["SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"]

# 소셜 인증 파이프라인 - 사용자가 소셜 인증을사용하여 인증할때 해당 소셜 프로필과 연관된 기본 사용자가 없는경우 새로운 user 객체 생성
# Python Social Auth 에 사용되는 기본 인증 파이프 라인
SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "account.authentication.create_profile",  # 소셜 유저를 생성한 후에 프로필 생성이 가능하다
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
]

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail',args=[u.username])
}

INTERNAL_IPS = ["mysite.com", "localhost", "127.0.0.1"]

if DEBUG:
    import mimetypes
    mimetypes.add_type('application/javascript','.js',True)
    mimetypes.add_type('text/css','.css',True)