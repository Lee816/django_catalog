from django.contrib import admin

from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "photo"]
    raw_id_fields = [
        "user"
    ]  # 데이터의 양이 많을 경우 드롭다운 방식은 어렵기 때문에 raw_id_fields 를 사용하면 input으로 변경됨
