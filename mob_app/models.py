from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from MOFU import settings
import email
from typing_extensions import Self
from unicodedata import name
import uuid



# Custom User manager
class UserManager(BaseUserManager):
    def create_user(self,email,name , password=None,password2=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email, name,password=None):
        user = self.create_user(
            email,
            password = password,
            name= name,
        
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#Custom User Model
class User(AbstractBaseUser):
    username = None
    email= models.EmailField(verbose_name='email address',max_length= 50,unique=True,)

    name = models.CharField(max_length=20)
    Gender = models.CharField(max_length=10)
    DOB = models.DateField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100)
    introduction_about_me_text = models.TextField(blank=True)
    introduction_about_me_voice = models.FileField(upload_to='uploads/', blank=True)
    invitation_code = models.CharField(max_length=32, blank=True)
    otp =models.CharField(max_length=8,null=True,blank=True)
    uid =models.UUIDField(default=uuid.uuid4)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    
    def has_module_perms(self,app_LabeL):
        "Dose the user have permissions to view the app 'app_label'?"
        return True
    

'''class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20, unique=True, default='+91')
    otp = models.CharField(max_length=8, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)

    # Add any additional fields or customizations as needed

    def __str__(self):
        return self.email'''
    
    
class Join(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Audio_Jockey = models.CharField(max_length=150)
    Jockey_Owner = models.CharField(max_length=150)
    Coins_Owner = models.CharField(max_length=150)
    Coins_Trader = models.CharField(max_length=150)


class Post(models.Model):
    post_name = models.CharField(max_length=100, default='')
    images = models.ImageField(upload_to='images/', blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userss')
    # followers_by = models.ManyToManyField(User, related_name='post_followers')
    # following_by = models.ManyToManyField(User, related_name='post_following')
    # def __str__(self):
    #     return self.post_name[0:10] + '...' + 'by' + self.user.email

    # @property
    # def posts_count(self):
    #     return self.posts.all().count()

    # @property
    # def followers_count(self):
    #     return self.followers.all().count()

    # @property
    # def following_count(self):
    #     return self.following.all().count()



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    images = models.ImageField(upload_to='images/')
    message = models.TextField(blank=True)
    #follow = models.ManyToManyField(User, related_name='following')
    Post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='follow')
    
class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")


class Stream(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="stream_following")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="stream_user")
    post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True)
    
# Create your models here.

