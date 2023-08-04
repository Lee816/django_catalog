from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "images"
    
    # 이 앱의 신호를 임포트 하여, 신호가 images 앱이 로드될때 임포트 되도록 한다.
    def ready(self):
        # import signal handlers
        import images.signals
