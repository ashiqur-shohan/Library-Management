
from django.urls import path
from .views import profile,user_logout,UserUpdateView,UserPasswordChangeView, UserRegistrationView, UserLoginView
 
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    # path('profile/', profile, name='profile'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/password_change/', UserPasswordChangeView.as_view(), name='password_change'),
]