# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class NoteBook(models.Model):
    '''単語帳のモデル'''
    title  = models.CharField(max_length=100)
    create_user = models.ForeignKey(get_user_model(),null=True,on_delete=models.CASCADE)
    context = models.TextField()
    def __str__(self):
        return self.title

    
class Post(models.Model):
    '''
    word:英単語
    trans:和訳
    interval:次の復習までの時間(日)
    e_factor:アイテムの簡単さ 1.3~2.5
    quo_res:アイテムへの回答の質　1~5
    '''
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(verbose_name='英単語を入力',max_length=50,blank=False,null=False)
    meaning = models.CharField(verbose_name='和訳',max_length=100)
    interval = models.FloatField(default=1)
    e_factor = models.FloatField(default=2.5)
    accuracy = models.FloatField(default=1)
    quo_res = models.IntegerField(default=5)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    notebook = models.ManyToManyField('NoteBook',blank=True)
    
    def __str__(self):
        return self.word