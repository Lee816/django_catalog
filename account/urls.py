from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "account"
urlpatterns = [
    # path("login/", views.user_login2, name="login"),
    path("", views.dashboard, name="dashboard"),
    # path("login/", auth_views.LoginView.as_view(), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]
