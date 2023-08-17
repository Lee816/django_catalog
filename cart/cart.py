from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

class Cart:
    def __init__(self,request) -> None:
        # 장바구니 초기화
        self.session = request.session
        # 현재 세션에 있는 장바구니를 가져옴
        cart = self.session.get(settings.CART_SESSION_ID)
        # 장바구니가 비어있을 경우
        if not cart:
            # 세션에 빈(딕셔너리) 장바구니 저장
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applired coupon
        self.coupon_id = self.session.get('coupon_id')
        
        # 장바구니에 제품 추가 또는 수량 변경
        # product - 장바구니에 추가되거나 업데이트 될 제품 인스턴스
        # quantity - 제품의 수량을 나타내며 기본값은 1
        # override_quantity - 수량을 주어진 수량으로 덮어쓸지(True) 새로운 수량을 기존 수량에 추가할지(False) 나타내는 불값
    def add(self,product,quantity=1,override_quantity=False):
        # str 을 사용하는 이유는 세션 데이터를 직렬화할때 JSON을 사용하며 JSON은 문자열 키만 허용하기 때문
        # 여기서는 제품의 ID 가 키가 되고 수량과 가격은 값으로 저장
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0,'price':str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] = quantity
        self.save()
        
    def save(self):
        # 세션이 '수정됨' 으로 표시되도록 설정 하여 저장
        self.session.modified = True
        
    def remove(self,product):
        # 장바구니에서 제품을 제거
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    # 장바구니 항목을 반복하고 Product 인스턴스에 액세스 하기 위한 메서드(데이터베이스에서 제품을 가져옴)
    def __iter__(self):
        product_ids = self.cart.keys()
        # 제품 객체를 가져와서 장바구니에 추가
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
            
    # 장바구니에 있는 총 항목수를 반환하는 메서드
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    # 장바구니에 있는 항목의 총 가격
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    # 세션에서 장바구니를 제거
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    # 쿠폰 관련 메서드
    
    # property로 정의하고 카트에 coupon_id 속성이 포함되어 있는 경우, 해당 ID로 Coupon 객체를 가져온다.
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
            return None
    
    # 카트에 쿠폰이 포함되어 있으면 쿠폰의 할인율을 검색해 카트의 총액에서 할인할 금액을 반환한다.
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)
    
    # get_discount() 메서드가 반환한 금액을 총액에서 빼고 할인이 적용된 카트의 총액을 반환한다.
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount