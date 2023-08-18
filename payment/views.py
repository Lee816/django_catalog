from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.urls import reverse

import stripe

from orders.models import Order
from mysite import settings

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id',None)
    order = get_object_or_404(Order,id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # Stripe checkout session data
        session_data = {
            'mode':'payment',
            'client_reference_id':order.id,
            'success_url':success_url,
            'cancel_url':cancel_url,
            'line_items':[]
        }
        # 주문 항목을 Stripe checkout 세션에 추가
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data':{
                    'unit_amount':int(item.price * Decimal('100')),
                    'currency':'usd',
                    'product_data':{
                        'name':item.product.name,
                    },
                },
                'quantity':item.quantity,
            })
        if order.coupon:
            # 쿠폰이 있는 경우 stripe.Coupon.create()를 사용하여 쿠폰을 생성
            # name - 주문 객체의 쿠폰 코드, percent_off - 주문 객체의 할인율, duration - 일회성 쿠폰임을 인식
            stripe_coupon = stripe.Coupon.create(name=order.coupon.code,percent_off=order.discount,duration='once',)
            # 쿠폰을 생성한 후 해당 쿠폰의 id를 session_data 딕셔너리에 추가
            session_data['discounts'] = [{'coupon':stripe_coupon.id}]
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url,code=303)
    else:
        return render(request,'payment/process.html',locals())

def payment_completed(request):
    return render(request,'payment/completed.html')

def payment_canceled(request):
    return render(request,'payment/canceled.html')