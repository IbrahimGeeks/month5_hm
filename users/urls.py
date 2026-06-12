from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_api_view),
    path('confirm/', views.confirm_api_view),
    path('login/', views.login_api_view),
]