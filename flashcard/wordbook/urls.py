from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'wordbook'

urlpatterns = [
    path('mypage/', views.MyPage.as_view(), name='page'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('delete_confirm', TemplateView.as_view(template_name='registration/delete_confirm.html'), name='delete-confirmation'),
    path('delete_complete', views.DeleteView.as_view(), name='delete-complete'),
    path('test/',views.MyNotebookListView.as_view(), name='test'),
    path('takepic/',views.TakePicture.as_view(),name='takepic'),
]