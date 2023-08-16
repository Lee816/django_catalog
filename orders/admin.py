from django.contrib import admin
from django.utils.safestring import mark_safe
import csv
import datetime
from django.http import HttpResponse

from .models import Order,OrderItem

# Register your models here.

def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''

order_payment.short_description = 'Stripe payment'

def export_to_csv(modeladmin,request,queryset):
    opts = modeladmin.model._meta
    # 파일이 포함된 응답임을 드라우저에 알림
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    # 응답 콘텐츠 유형을 지정
    response = HttpResponse(content_type='text/csv')
    # 파일을 나타내기 위한 헤더 추가
    response['Content-Disposition'] = content_disposition
    # 응답에 대한 작정자 생성
    writer = csv.writer(response)
    # 모델의 필드를 동적으로 가져오기 위한 _meta 옵션의 get_fields()메서드를 사용하며 다대다,일대다 관계는 제외한다.
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # Write a first row with header information
    # 헤더행을 포함한 첫 번째 행에 헤더 정보를 작성
    writer.writerow([field.verbose_name for field in fields])
    
    # Write data rows
    # QuerySet을 반봅해 각 객체에 대한 행을 작성하며 CSV의 출력 값은 문자열 이어야 하므로 datetime 객체를 형식에 맞게 문자열로 변환
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj,field.name)
            if isinstance(value,datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

# 함수의 short_desciption 속성을 사용해 관리사이트에 표시할 이름을 설정
export_to_csv.short_desciption = 'Esport to CSV'

# OrderItem 모델을 OrderAdmin 클래스의 인라인으로 포함하기 위해 ModelInline 클래스 사용
# 인라인은 관련 모델과 동일한 편집 페이지에 모델을 포함하는데 사용
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','address','postal_code','city','paid',order_payment,'created','updated']
    list_filter = ['paid','created','updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]