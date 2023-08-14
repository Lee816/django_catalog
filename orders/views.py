from django.shortcuts import render, redirect
from django.urls import reverse

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

# Create your views here.

def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
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