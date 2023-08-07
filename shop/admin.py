from django.contrib import admin

from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    # prepopulated_fields 는 slug 필드에 name필드의 내용을 자동으로 입력해 준다.
    prepopulated_fields = {'slug': ('name',)}
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','available','created','updated']
    list_filter = ['available','created','updated']
    # 목록 표시 페이지에서 편집 가능한 필드를 설정하며 list_display에도 같이 등록 되어 있어야 한다.
    list_editable = ['price','available']
    prepopulated_fields = {'slug': ('name',)}