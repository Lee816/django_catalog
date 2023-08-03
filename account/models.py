from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class Contact(models.Model):
    # 관계를 생성하는 사용자에 대한 외래키
    user_from = models.ForeignKey('auth.User',related_name='rel_from_set',on_delete=models.CASCADE)
    # 팔로우 되는 사용자에 대한 외래키
    user_to = models.ForeignKey('auth.User',related_name='rel_to_set',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'
    
user_model = get_user_model()
user_model.add_to_class('following',models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False))