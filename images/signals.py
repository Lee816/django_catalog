from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Image

# receiver() 데코레이터를 사용하여 함수를 수신 함수로 등록
# m2m_changed 신호에 연결하고 Image.users_like.through에 함수를 연결하여 이 함수가 해당 sender에 의해 발생한 m2m_changed 신호에서만 호출되도록한다.
# 신호 수신 함수를 등록하는 다른 방법은 Signal 객체의 connect() 메서드를 사용하는것
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()