"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    "posts": PostSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls", namespace="blog")),
    path("sitemap.xml",sitemap,{"sitemaps": sitemaps},name="django.contrib.sitemaps.views.sitemap",),
    path("account/", include("account.urls")),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path('images/',include('images.urls', namespace='images')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('shop/',include('shop.urls',namespace='shop')),
    path('cart/',include('cart.urls',namespace='cart')),
    path('orders/',include('orders.urls',namespace='orders')),
    path('payment/',include('payment.urls',namespace='payment')),
    path('coupons/',include('coupons.urls',namespace='coupons')),
    path('rosetta/',include('rosetta.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
