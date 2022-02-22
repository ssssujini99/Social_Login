from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView
from . import views

urlpatterns = [
    # 소셜 로그인
    path('api/token/', jwt_views.TokenObtainPairView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view()), # access-token refresh
    path('hello/', views.HelloView.as_view()),

    path('account/login/kakao/', views.kakao_login, name='kakao_login'),
    path('account/login/kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('account/logout/kakao/', views.kakao_logout, name="kakao_logout"),
    path('account/resign/kakao/', views.kakao_resign, name="kakao_resign"),
    ]