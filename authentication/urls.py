from . import views
from django.urls import path

app_name = 'user_authentication'

urlpatterns = [
    path('register/', views.RegisterEndpoint.as_view(), name = 'register'),
    path('login/', views.LoginEndpoint.as_view(), name = 'login'),
    path('logout/', views.LogoutEndpoint.as_view(), name = 'logout')
]