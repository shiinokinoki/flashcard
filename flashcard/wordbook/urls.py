from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'wordbook'

urlpatterns = [
    path('home/', views.MyNotebookListView.as_view(), name='home'),#HTMLをそのまま見る
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('delete_confirm', TemplateView.as_view(template_name='registration/delete_confirm.html'), name='delete-confirmation'),
    path('delete_complete', views.DeleteView.as_view(), name='delete-complete'),
    path('takepic/',views.TakePicture.as_view(),name='takepic'),#HTMLをそのまま見る
    # path('takepic/detimg/',views.GetImage(),name='detimg'),
    path('registerlist/',views.MakeRegisterListView.as_view(),name='registerlist'),
    # path('registerlist/registered/',views.GetChecklist.as_view(),name='registered'),
    # path('learning/',views.GetAnswers.as_view(),name=''),
    path('post_list/', views.MyPostListView.as_view(), name='post_list'),
    path('post/<uuid:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<uuid:pk>/edit', views.PostUpdateView.as_view(),name='post_update'),
    path('post/<uuid:pk>/delete',views.PostDeleteView.as_view(),name='post_delete'),
]