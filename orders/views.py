from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

# Create your views here.

def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # 데이터베이스에 바로 적용하지 않고 쿠폰이 있을경우 쿠폰 정보와 함께 저장
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])

            # clear the cart
            cart.clear()
            # 비동기 실행
            order_created.delay(order.id)
            # 세션에 주문정보 등록
            request.session['order_id'] = order.id
            # 결제시스템에 리다이렉트
            return redirect(reverse('payment:process'))
            
            # return render(request,'orders/order/created.html', {'order':order})

    else:
        form = OrderCreateForm()
            
    return render(request,'orders/order/create.html',{'cart':cart,'form':form})

# 페이지를 요청하는 사용자의 is_active와 is_staff 필드가 모두 True인지 확인
# 주어진 ID로 Order 객체를 가져와서 주문을 표시하기 위한 템플릿을 렌더링
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'admin/orders/order/detail.html', {'order':order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # 장고에서 제공하는 render_to_string()함수를 사용하여 orders/order/pdf.html을 렌더링
    html = render_to_string('orders/order/pdf.html',{'order':order})
    # application/pdf 콘텐츠 유형을 지정
    # 파일이름을 지정하기 위해 Content-Disposition 헤더를 포함하는 새 HttpResponse 객체를 생성
    response = HttpResponse(content_type='applecaion/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    # WeasyPrint 를 사용하여 렌더링된 HTML 코드에서 PDF 파일을 생성하고 HttpResponse 객체인 response에 파일을 쓰기
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT/'css/pdf.css')])

    return response