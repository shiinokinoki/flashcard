# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    get_user_model, logout as auth_logout,
)

from .forms import UserCreateForm
from .models import User, NoteBook, Post

from wordbook.pymodule.read_json import ReadJson as readjson
from wordbook.pymodule.machine_learning.detect import All_process

import cv2
import random

User = get_user_model()

class Top(generic.TemplateView):
    '''
    Topページ表示
    '''
    template_name = 'top.html'

class MyNotebookListView(generic.ListView):
    '''
    ユーザーごとのホーム画面
    '''
    model = NoteBook
    def get_queryset(self):
        user = self.request.user
        return NoteBook.objects.filter(create_user=user)


class MyPostListView(generic.ListView):
    '''
    ユーザー単語全リスト
    '''
    model = Post
    template_name = 'wordbook/post_list.html'
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(create_user=user)


class PostDetailView(generic.DetailView):
    '''
    '''
    model = Post
    template_name = 'wordbook/post_detail.html'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['name', 'meaning', 'notebook']


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('wordbook:post_list')



# # class MakeRegisterListView(LoginRequiredMixin, generic.ListView):
#     template_name = 'wordbook/register_list.html'
#     model = Post
#     def get_queryset(self):
#         count =0
#         path = './wordbook/data/json/dict_sample.json'
#         scanned_dic = readjson(path=path)
#         user = self.request.user
#         for word in scanned_dic:
#             for meaning in word['meaning']:
#                 result, created = Post.objects.get_or_create(name = word['name'],meaning=meaning,create_user=user)
#                 if created:
#                     count +=1
#         return Post.objects.filter(create_user=user).order_by('-date_joined')[:count]


def makeregisterlist(request):
    '''
    認識結果のjsonを読み込んで辞書化，これをHTMLに渡す
    '''
    template_name = 'wordbook/register_list.html'
    model = Post
    count =0
    path = './wordbook/data/json/dict_sample.json'
    scanned_dic = readjson(path=path)
    word_list =[]
    for word in scanned_dic:
        word_list.append(word['name'])
    context = {
        'word_list':word_list,
    }
    return render(request, 'wordbook/register_list.html', context=context)



def getimage(request):
    if request.method == 'POST':
        posted_img = request.FILES['image']
        cv2.imwrite('./wordbook/pymodule/machine_learning/result.png',posted_img)
        detector = All_process()
        return redirect('registerlist/')
    # else:
    #     return redirect('https://google.com')


class GetAnswers(generic.ListView):
    def post(self, request, *args, **kwargs):
        checks_value = request.POST.getlist('checks[]')
        
        
class TakePicture(generic.TemplateView):
    template_name = 'takepic.html'
    
def makeQuestAtRandom(self,request):
    num = 3
    num_choices = 4
    user = self.request.user
    posts = Post.objects.order_by('?')[:num]
    names = []
    choices = []
    ans = []
    for i in posts:
        names.append(i.values('name'))
        choices_cand = Post.objects.order_by('?')[:num_choices-1]
        cho = []
        cho.append(i.values('meaning'))
        for m in choices_cand:
            cho.append(m.values('meaning'))
        choices.append(cho)
    
    if len(choices)!=num_choices:
        print('error')
    random.shuffle(choices)
    
    for i in names:
        tmp = []
        for m in choices:
            if m == i:
                tmp.append(True)
            else:
                tmp.append(False)
        ans.append(tmp)

    data = {}
    for li1,li2,li3 in zip(choices,ans,names):
        dic1={}
        dic1[ch[0]]=li1
        dic1[ch[1]]=li2
        data[li3]=dic1
    return JsonResponse(data)

def makeQuestMistake(self,request):
    num = 3
    num_choices = 4
    user = self.request.user
    posts = Post.objects.order_by('')[:num]
    names = []
    choices = []
    ans = []
    for i in posts:
        names.append(i.values('name'))
        choices_cand = Post.objects.order_by('?')[:num_choices-1]
        cho = []
        cho.append(i.values('meaning'))
        for m in choices_cand:
            cho.append(m.values('meaning'))
        choices.append(cho)
    
    if len(choices)!=num_choices:
        print('error')
    random.shuffle(choices)
    
    for i in names:
        tmp = []
        for m in choices:
            if m == i:
                tmp.append(True)
            else:
                tmp.append(False)
        ans.append(tmp)

    data = {}
    for li1,li2,li3 in zip(choices,ans,names):
        dic1={}
        dic1[ch[0]]=li1
        dic1[ch[1]]=li2
        data[li3]=dic1
    return JsonResponse(data)




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



