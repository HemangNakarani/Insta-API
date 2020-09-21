from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import HelloView, RegisterUserView, ManageUserView, GetFollowersView, GetFollowingsView, \
    UserProfileView, FollowUserView, RequestsView, RequestProcessView
app_name = 'user'

urlpatterns = [
    path('', HelloView.as_view(), name='hello'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('@me/', ManageUserView.as_view(), name='update'),
    path('requests/', RequestsView.as_view(), name='update'),
    path('<slug:username>/', UserProfileView.as_view(), name='user-profile'),
    path('<slug:username>/request/', RequestProcessView.as_view(), name='update'),
    path('<slug:username>/followers/', GetFollowersView.as_view(), name='get-followers'),
    path('<slug:username>/followings/', GetFollowingsView.as_view(), name='get-followings'),
    path('<slug:username>/follow/', FollowUserView.as_view(), name='toggle-follow'),
]
