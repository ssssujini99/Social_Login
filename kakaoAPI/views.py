from django.shortcuts import redirect, HttpResponse
import requests
import os, environ

env = environ.Env(
    DEBUG=(bool, False)
)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# code 요청
def kakao_login(request):
    app_rest_api_key = env('REST_API_KEY')
    redirect_uri = env('REDIRECT_URI')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )


# token 요청 및 정보 조회
def kakao_callback(request):
    app_rest_api_key = env('REST_API_KEY')
    redirect_uri = env('REDIRECT_URI')
    client_secret = env('SECRET')

    code = request.GET.get('code')
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={code}"
    )
    token_req_json = token_req.json()
    access_token = token_req_json.get("access_token")
    print(access_token)

    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    print(profile_json)

    kakao_account = profile_json.get("kakao_account")
    profile = kakao_account.get("profile")
    nickname = profile.get("nickname")
    email = kakao_account.get("email")
    print(nickname, email)
    return HttpResponse("성공")