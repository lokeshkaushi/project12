from rest_framework import serializers
from .models import *
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from rest_framework import serializers





class customuser_serializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['email','phone','forget_password_token']

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ('name','Gender','DOB','phone','location','email','password','introduction_about_me_text','introduction_about_me_voice','invitation_code')
class RegisterSerializer12(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','location']

class JoinSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Join
        fields = ['user','Audio_Jockey','Jockey_Owner','Coins_Owner','Coins_Trader']



class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()    
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if user and user.is_active:
           return attrs

    


class User_Post_serializer(serializers.ModelSerializer):
    # total_followers = serializers.SerializerMethodField()
    # total_following = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [ 'user', 'post_name','images','description']

        #fields = [ 'user', 'post_name','images','description','followers_by','total_followers','following_by','total_following']

    # def get_total_followers(self, instance):
    #     return instance.followers_by.count()
    
    # def get_total_following(self, instance):
    #     return instance.following_by.count()
    

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
    
class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = '__all__'
    
class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['user','images','message','post']

class ProfileSerializer12(serializers.ModelSerializer):
    user = RegisterSerializer12(many=False, read_only=True, required=False)
    follow = StreamSerializer(many=False, read_only=True, required=False)
    # total_post = serializers.SerializerMethodField()
    # follow = FollowSerializer(many=False, read_only=True, required=False)
    
    class Meta:
        model = Profile
        fields = ['user','images','message','Post','follow']
    
    
