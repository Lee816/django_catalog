from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Action(models.Model):
    user = models.ForeignKey('auth.User',related_name='actions',on_delete=models.CASCADE)
    verb = models.CharField(max_length=255) # 동작의 설명을 위한 필드
    created = models.DateTimeField(auto_now_add=True)
    
    # ContentType 모델을 가리키는 외래키
    target_ct = models.ForeignKey(ContentType,blank=True,null=True,related_name='target_obj',on_delete=models.CASCADE)
    # 관련 객체의 기본키를 저장하기 위한 필드
    target_id = models.PositiveIntegerField(null=True,blank=True)
    # 앞의 두 필드의 조합을 기반으로 관련 객체를 가리키는 필드
    target = GenericForeignKey('target_ct','target_id')

    class Meta:
        indexes = [
            models.Index(fields = ['-created']),
            models.Index(fields = ['target_ct','target_id']),
        ]
        
        ordering = ['-created']