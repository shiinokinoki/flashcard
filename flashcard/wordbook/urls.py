from django.urls import path
from . import views

app_name = 'wordbook'

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('top/', views.Top.as_view(), name='top'),
    path('logout/', views.Logout.as_view(), name='logout'),
]