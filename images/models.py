from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Image(models.Model):
    # 해당 이미지를 등록한 사용자이며 일대다의 관계를 가진다. 사용자는 다 이미지, 이미지는 일 사용자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE,
    )
    # 이미지 제목
    title = models.CharField(max_length=200)
    # URL을 만들기 위한 짧은 레이블
    slug = models.SlugField(max_length=200, blank=True)
    # 이미지의 원본 URL
    url = models.URLField(max_length=2000)
    # 이미지 파일
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    # 이미지의 설명
    description = models.TextField(blank=True)
    # 데이터베이스에 등록된 날짜
    created = models.DateField(auto_now_add=True)

    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="images_liked", blank=True
    )

    class Meta:
        # created 필드에 대한 내림차순으로 데이터베이스 인덱스를 정의
        # 인덱스는 쿼리 성능을 향상시키기 때문에 조건으로 자주 사용하는 필드에 대해 인덱스를 생성하는 것이 좋다.
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"]

    def __str__(self):
        return self.title

    # save()메서드를 재정의 하여 title 필드의 값을 기반으로 slug 필드를 채워서 생성
    # slug 필드에 값이 없는 경우, slugify()함수를 사용하여 이미지의 제목에서 자동으로 슬러그를 생성
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # 슬러스를 먼저 채우고
        super().save(*args, **kwargs)  # 객체 저장

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])