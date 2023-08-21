from django import forms
from django.utils.translation import gettext_lazy as _

PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    # 사용자가 1부터 20 사이의 수량을 선택할 수 있다. 입력을 정수로 변환하기 위해 TypedChoiceField 필드와 coerce=int 속성 사용
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int,label=_('Quantity'))
    # 장바구니에 있는 기존 수량에 대해 주어진 수량을 추가해야하는False 아니면 주어진 수량으로 기존수량을 덮어쓰는지True 나타내며, 사용자에게 표시하지 않기위해 HiddenInput 위젯 사용
    override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
