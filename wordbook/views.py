# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    get_user_model, logout as auth_logout,
)

from .forms import UserCreateForm,NoteBookForm,ImageForm
from .models import User, NoteBook, Post, Image
from wordbook.pymodule.read_json import ReadJson as readjson
from wordbook.pymodule.machine_learning.detect import All_process
from wordbook.pymodule.sm2 import calculate_interval_and_e_factor

import cv2
import random
import json
import base64
import numpy as np

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
    template_name = 'wordbook/NoteBook_list.html'
    model = NoteBook
    def get_queryset(self):
        user = self.request.user
        return NoteBook.objects.filter(create_user=user)

class NotebookCreateView(generic.CreateView):
    model = NoteBook
    form_class = NoteBookForm
    template_name = "wordbook/createNBform.html"
    def get_form(self):
        form = super(NotebookCreateView, self).get_form()
        form.fields['title'].label = '単語帳名'
        return form
    def form_valid(self, form):
        post = form.save(commit=False)
        post.create_user = self.request.user
        post.save()
        return redirect("wordbook:home")
    
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
    単語詳細
    '''
    model = Post
    template_name = 'wordbook/post_detail.html'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['name', 'meaning', 'notebook']
    success_url = reverse_lazy('wordbook:post_list')


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
    とってきたjsonをそのままレスポンスしたい
    '''
    template_name = 'wordbook/register_list.html'
    model = Post
    count =0
    path = './save.json'
    
    word_li = readjson(path=path)
    # word_list =[]
    # for word in scanned_dic:
    #     word_list.append(word['name'])
    # context = {
    #     'word_list':word_list,
    # }
    data = {}
    dic_li = []
    for i,d in enumerate(word_li):
        dic = {}
        dic['id'] = i
        dic['word'] = d['name']
        dic['mean'] = d['meaning']
        dic_li.append(dic)
    
    data["pagename"] = "register_list"
    data["data"] = dic_li
    data["url"] = ''
    context = {
        "value":data,
    }
    return render(request, 'wordbook/register_list.html',context=context)

def upload(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            data = {
                'pagename':'registerlist',
                'url':'registerlist/',
            }
            context = {'value':data}
            path = './wordbook/pymodule/machine_learning/receive.png'
            detector = All_process()
            detector.run(img_path=path)
            word_li = readjson(path=path)
            data = {}
            dic_li = []
            for i,d in enumerate(word_li):
                dic = {}
                dic['id'] = i
                dic['word'] = d['name']
                dic['mean'] = d['meaning']
                dic_li.append(dic)
            
            data["pagename"] = "registerlist"
            data["data"] = dic_li
            data["url"] = 'registering/'
            context = {
                "value":data,
            }
            return render(request, 'wordbook/register_list.html',context=context)
    else:
        form = ImageForm()

    context = {'form':form}
    return render(request, 'takepic.html', context)

# def getimage(request):
#     if request.method == 'POST':
#         img_str = request.Form['image']
#         # path = './test_img.txt'
#         # with open(path,mode = 'w') as f:
#         #     f.write(img_str)
#         posted_img = base64.b64decode(img_str)
#         jpg=np.frombuffer(posted_img,dtype=np.uint8)
#         #raw image <- jpg
#         img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
#         cv2.imwrite('./wordbook/pymodule/machine_learning/receive.png',img)
#         path = './wordbook/pymodule/machine_learning/receive.png'
#         detector = All_process()
#         detector.run(img_path=path)
#         return redirect('wordbook:registerlist')
#     else:
#         return redirect('wordbook:takepic')

def getRegister(request):
    if request.method == 'POST':
        user = request.user
        json_str = request.body.decode('utf-8')
        json_data = json.loads(json_str)['data']
        for item in json_data:
            p = Post.objects.create(name=item['word'],meaning=item['mean'])
        return redirect('wordbook:home')
    else:
        return redirect('wordbook:takepic')

def getQuestResult(request):
    '''
    jsonは{'単語':'正誤'}で返してもらう
    e-factorのパラメータ更新
    '''
    if request.method == 'POST':
        user = request.user
        json_str = request.body.decode('utf-8')
        json_data = json.loads(json_str)
        # path = './test.txt'
        # with open(path,mode = 'w') as f:
        #     f.write(json_str)
        ans_li = request.values()
        posts = Post.objects.filter(create_user=user)
        
        for word,ans in zip(names,ans_li):
            post = posts.filter(name=word)[0]
            _interval = post.interval
            _e_factor = post.e_factor
            if ans_li:
                interval, e_factor=calculate_interval_and_e_factor(_interval,_e_factor,5)
            else:
                interval, e_factor=calculate_interval_and_e_factor(_interval,_e_factor,1)
            post.interval = interval
            pot.e_factor = e_factor
            post.save()
        
        return redirect('wordbook:home')
    else:
        return redirect('wordbook:result')
        

def takepicture(request):
    data = {'url':'takepic/detimg/','pagename':'takepic'}
    context = {'value':data}
    return render(request, 'takepic.html',context=context)
    
def makeQuestAtRandom(request,pk):
    '''
        任意の単語数の問題を作成，辞書をJsonResponseでJsonとして返す．
    '''
    debug = False
    if debug == False:
        num_word = 3 #問題の単語数
        num_choices = 4 # 選択肢の数
        user = request.user  #現在のユーザ
        try:
            posts = Post.objects.filter(notebook__pk=pk).order_by('?')[:num_word]  #必要とする単語数分のデータ
        except:
            raise Http404('not exist')

        names = []
        means = []
        flags = []
        # ids = []
        corrects = []
        
        if Post.objects.all().count() < num_choices:
                raise Http404('not exist')
        for post in posts:
            names.append(post.name)
            corrects.append(post.meaning)
            while True:
                #単語がダブらないようにする．
                flag=True
                choices_cand = Post.objects.order_by('?')[:num_choices - 1]
                for meaning in choices_cand:
                    if corrects[-1] == meaning.meaning:
                        flag = False
                        break
                if flag:
                    break
                        
            choice_mean = []
            choice_mean.append(post.meaning)
            for meaning in choices_cand:
                choice_mean.append(meaning.meaning)
            random.shuffle(choice_mean)
            means.append(choice_mean)
            # ids.append(post.values('id'))
        
        for correct,choices in zip(corrects,means):
            correct_or_wrong = []
            for choice in choices:
                if choice == correct:
                    correct_or_wrong.append('correct')
                else:
                    correct_or_wrong.append('wrong')
            flags.append(correct_or_wrong)

        data = {}
        ans=[]
        for id_,mean,flag,name in zip(range(len(flags)),means,flags,names):
            dic = {}
            dic['word'] = name
            dic['mean'] = mean
            dic['id'] = id_
            dic['flag']=flag
            dic['result'] = 'nan'
            ans.append(dic)

        
        data['url'] = 'learning/result/'
        data['pagename'] = 'question'
        data['data']=ans

    else:
        data = {
            'url':'learning/result/',
            'pagename':'question',
            "data":
            [
                {
                    'id':0,
                    'word':'fact',
                    'mean':['意味１','意味2','意味3','意味4'],
                    'flag':['correct','wrong','wrong','wrong'],
                    'result':'nan',
                },
                {
                    'id':1,
                    'word':'red',
                    'mean':['意味１','意味2','意味3','意味4'],
                    'flag':['wrong','correct','wrong','wrong'],
                    'result':'nan',
                },
                
                {
                    'id':2,
                    'word':'blue',
                    'mean':['意味１','意味2','意味3','意味4'],
                    'flag':['wrong','wrong','wrong','correct'],
                    'result':'nan',
                },
            ]
        }

    context = {
        "value":data,
        }
    
    return render(request, 'wordbook/questions.html',context=context)



def makeQuestMistake(request):
    num = 3
    num_choices = 4
    user = request.user
    posts = Post.objects.order_by('interval')[:num]
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
        data[li3]=[dic1]
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
        # user.is_active = False
        # user.save()
        user.delete()
        auth_logout(self.request)
        return render(self.request,'registration/delete_complete.html')



