from django.urls import path
from .views import UserSignupAPIView, UserDetailsUpdateAPIView, AdminAPIView, PostsAPIView, UserSigninAPIView


urlpatterns = [
    path('signup/', UserSignupAPIView.as_view(), name="user-signup"),
    path('signin/', UserSigninAPIView.as_view(), name="user-signin"),
    path('details/', UserDetailsUpdateAPIView.as_view(), name="user-details"),
    path('users-by-admin/', AdminAPIView.as_view(), name='get-users-by-admin'),
    path('users/<int:pk>/', AdminAPIView.as_view(), name='update-delete-user'),
    path('create-posts/', PostsAPIView.as_view(), name='create-post'),
    path('posts/user/', PostsAPIView.as_view(), name='user-posts'),
]
