from django.contrib import admin
from django.urls import path ,include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *


# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', Register.as_view(), name="Register"),
    path('join/', join_create, name='join-create'),
    # path('login',views.login,name='login'),
    path('login_otp/', login_view, name="login"),
    path('otp/<uid>/', otp , name='otp'),
    path('user_post/',User_Post.as_view(),name='user_post'),
    # path('Followers/<int:id>',views.Followers_Post,name='Followers_post'),
    # path('Following/<int:id>',views.Following_Post,name='Following_post'),
    # path('Create_Post',views.Create_Post,name='Create_Post'),
    path('profile/', ProfileAPIView.as_view(), name='profile-api'),
    path('follower-count/<int:user_id>/', FollowerCountView.as_view(), name='follower_count'),
    path('following-post-count/<int:user_id>/', FollowingAndPostCountView.as_view(), name='following_post_count'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('api_login/', LoginAPIView.as_view(), name='api_login'),
    # path('loginotp/', LoginView.as_view(), name='login'),
    # path('login/',views.user_Login,name='login')
    # path('login/', LoginView.as_view(), name='login'),
    path('login/facebook/', facebook_login, name='facebook-login'),
    path('login/facebook/callback/', facebook_login_callback, name='facebook-login-callback'),
]