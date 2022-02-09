from django.urls import path
from . import views

urlpatterns = [
    # 소셜 로그인
    path('account/login/kakao/', views.kakao_login, name='kakao_login'),
    path('account/login/kakao/callback/', views.kakao_callback, name='kakao_callback'),
    ]