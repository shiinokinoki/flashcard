# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    get_user_model, logout as auth_logout,
)
from .forms import UserCreateForm
from wordbook.models import User, NoteBook, Post
from wordbook.pymodule.read_json import ReadJson as readjson



User = get_user_model()

class Top(generic.TemplateView):
    template_name = 'top.html'

class MyPage(generic.TemplateView):
    template_name = 'page.html'

class MyNotebookListView(generic.ListView):
    model = NoteBook
    def get_queryset(self):
        user = self.request.user
        return NoteBook.objects.filter(create_user=user)

class MakeRegisterListView(LoginRequiredMixin, generic.ListView):
    template_name = 'wordbook/register_list.html'
    model = Post
    def get_queryset(self):
        count =0
        path = './wordbook/data/json/dict_sample.json'
        scanned_dic = readjson(path=path)
        user = self.request.user
        for word in scanned_dic:
            for meaning in word['meaning']:
                count +=1
                Post.objects.create(name = word['name'],meaning=meaning,create_user=user)
        return Post.objects.filter(create_user=user).order_by('-date_joined')[:count]


    
class TakePicture(generic.TemplateView):
    template_name = 'takepic.html'


#Auth認証 関連

class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        return render(self.request,'registration/profile.html')


class DeleteView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user.email)
        user.is_active = False
        user.save()
        auth_logout(self.request)
        return render(self.request,'registration/delete_complete.html')

