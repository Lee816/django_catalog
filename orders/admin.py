from django.contrib import admin

from .models import Order,OrderItem

# Register your models here.

# OrderItem 모델을 OrderAdmin 클래스의 인라인으로 포함하기 위해 ModelInline 클래스 사용
# 인라인은 관련 모델과 동일한 편집 페이지에 모델을 포함하는데 사용
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','address','postal_code','city','paid','created','updated']
    list_filter = ['paid','created','updated']
    inlines = [OrderItemInline]