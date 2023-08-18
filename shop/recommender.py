import redis
from django.conf import settings

from .models import Product

# redis 연결
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# 이 클래스를 사용하여 제품 구매를 저장하고 주어진 제품 또는 제품 목록에 대한 제품 추천을 검색할 수 있다.
class Recommender:
    # Product 객체의 ID를 받아 해당 제품과 구매된 상품이 저장된 Redis 키를 반환한다.
    def get_product_key(self,id):
        return f'product: {id}:purchased_with'

    # 함께 구매된 Product 객체 목록을 받는다.
    def products_bought(self,products):
        # 제품 목록에서 제품의 ID를 리스트로 생성
        product_ids = [p.id for p in products]
        # 제품 ID를 순회하며 동일한 제품은 건너뛰고 각 체줌과 함께 구매죈 제품을 얻을 수 있다.
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    # get_product_key() 메서드를 사용해 Redis 제품키를 가져와 제품 ID를 정렬된 집합에 포함된 각 제품 ID의 점수를 1씩 증가시킨다.
                    r.zincrby(self.get_product_key(product_id),1,with_id)
                 
    
    # products - 제품 추천을 위한 Product 객체 목록, max_result - 반환할 추천 결과의 최대 개수
    def suggest_products_for(self, products, max_results=6):
        # 제품의 ID를 리스트로 반환
        product_ids = [p.id for p in products]
        # 제품이 하나만 있는 경우
        if len(products) == 1:
            # 주어진 제품과 함께 구매된 제품의 ID를 가져와 전체 구매 횟수에 따라 정렬
            suggestions = r.zrange(self.get_product_key(product_ids[0]),0,-1,desc=True)[:max_results]
        # 제품이 여러개 있는 경우
        else:
            # 제품 ID를 결합하여 임시 Redis 키를 생성한다. 이 키는 제품들의 점수를 집계하는데 사용
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(id) for id in product_ids]
            # zunionstore 는 주어진 키들의 정렬된 집합을 결합하고 요소들의 점수를 집계하여 새로운 Redis 키에 저장
            r.zunionstore(tmp_key,keys)
            # 추천을 받고 있는 제품들이 동일하게 나오는 것을 방지하기 위해 zrem을 사용하여 제거
            r.zrem(tmp_key,*product_ids)
            # zrange를 이용하여 임시 키에서 제품 ID를 점수에 따라 정렬하여 가져온다.
            suggestions = r.zrange(tmp_key,0,-1,desc=True)[:max_results]
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products
    
    
    # 추천 엔진 초기화
    def clear_purchases(self):
        for id in Product.objects.values_list('id',flat=True):
            r.delete(self.get_product_key(id))