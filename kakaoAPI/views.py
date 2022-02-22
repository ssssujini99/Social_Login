from django.shortcuts import redirect, HttpResponse, render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import requests
import os, environ
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


User = get_user_model()

# JWT 발급 함수
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

env = environ.Env(
    DEBUG=(bool, False)
)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

access_token = ""


class HelloView(APIView):
    def get(self, request):
        user = request.user
        print(user)
        content = {'message': 'Hello, World!'}
        return Response(content)


# code 요청 -> 프론트 부분
@api_view(['GET'])
@permission_classes([AllowAny])
def kakao_login(request):
    app_rest_api_key = env('REST_API_KEY')
    redirect_uri = env('REDIRECT_URI')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )


# 카카오 회원가입 & 로그인
def kakao_callback(request):
    app_rest_api_key = env('REST_API_KEY')
    redirect_uri = env('REDIRECT_URI')
    client_secret = env('SECRET')

    code = request.GET.get('code')
    print(code)
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={code}"
    )
    token_req_json = token_req.json()
    global access_token
    access_token = token_req_json.get("access_token")
    refresh_token = token_req_json.get("refresh_token")
    print("access_token: ", access_token)
    print("refresh_token: ", refresh_token)

    kakao_api_response = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    kakao_api_response = kakao_api_response.json()
    user_id = kakao_api_response.get('id')
    #if user_id is None:
    #    return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
    username = f'user{user_id}'

    realname = kakao_api_response.get('properties').get('nickname')
    print(username, realname)

    try:
        user = User.objects.get(username=username)
        print("기존 유저")

    except:
        user = User(username=username, realname=realname)
        user = user.save()
        user = User.objects.get(username=username)
        print("새로운 유저")

    response = {'username': username, 'token': get_tokens_for_user(user)}
    print(response)
    return JsonResponse(response, status=200)


# 로그아웃 -> 사용자의 access_token, refresh_token 모두 만료시킴
def kakao_logout(request):
    data = requests.post("https://kapi.kakao.com/v1/user/logout",
                  headers={"Authorization": f"Bearer {access_token}"},
                  )
    print(data.json())
    return HttpResponse("로그아웃")


# 연결 끊기 -> 사용자와 앱의 연결을 해제(카카오 로그인을 통해 서비스에 가입한 사용자가 탈퇴하거나, 카카오 로그인 연동 해제를 요청할 경우)
def kakao_resign(request):
    #print("access_token", access_token)
    access_token = "m2erjTiDuEz4SzHrCMVvhBQHVj6vcE31faFUZAo9dNoAAAF_F4fRwQ"

    data = requests.post("https://kapi.kakao.com/v1/user/unlink",
                         headers={"Authorization": f"Bearer {access_token}"},
                         )
    print(data.json())
    return HttpResponse("연결종료")