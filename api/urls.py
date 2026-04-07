from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

app_name = "api"

urlpatterns = [
    path(
        "auth/login/",
        jwt_views.TokenObtainSlidingView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("auth/register/", views.RegisterApi.as_view(), name="auth_user_create"),
    path("save-code/", views.save_code, name="save_code"),
    path("isLocation-exists/", views.isLocation_coded, name="isLocation_exists"),
    path("get_code_infos/", views.get_code, name="get_code_infos"),
    path("my-addresses/", views.get_my_addresses, name="my_addresses"),
    path("generate/", views.generate_code, name="generate"),
]
