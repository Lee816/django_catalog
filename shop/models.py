from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
        models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
class Product(models.Model):
    # Category 모델에 대한 외래키이며 1:N 관계이다. 제품은 하나의 카테고리에 속하고, 하나의 카테고리는 여러개의 제품이 속한다.
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    # 보기좋은 URL을 만들기 위한 슬러그
    slug = models.SlugField(max_length=200,allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    # 고정소수점(decimal.Decimal)을 사용하여 가격을 저장한다. max_digits 속성은 최대 숫자 자리수를 설정하고 decimal_places 속성으로 소수 자리수를 설정한다.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # 제품의 활성화 비활성화
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id','slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        
    def __str__(self):
        return self.name
