# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser,UnicodeUsernameValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_(
            'Required. 150 characters or fewer.'
            ' Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'



class NoteBook(models.Model):
    '''単語帳のモデル'''
    name = models.CharField(max_length=100)
    create_user = models.ForeignKey(get_user_model(),null=True,on_delete=models.CASCADE)
    context = models.TextField()
    
    
    
class Post(models.Model):
    '''
    word:英単語
    trans:和訳
    interval:次の復習までの時間(日)
    e_factor:アイテムの簡単さ 1.3~2.5
    quo_res:アイテムへの回答の質　1~5
    '''
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    word = models.CharField(verbose_name='英単語を入力',max_length=50,blank=False,null=False)
    trans = models.CharField(verbose_name='和訳',max_length=100)
    interval = models.FloatField(default=1)
    e_factor = models.FloatField(default=2.5)
    accuracy = models.FloatField(default=1)
    quo_res = models.IntegerField(default=5)
    
    notebook = models.ManyToManyField('NoteBook',null=True)