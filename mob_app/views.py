from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
#from .helper import send_forget_password_mail
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import generics ,response
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view,parser_classes
import random
from django.contrib.auth import authenticate,logout,login
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser ,JSONParser
import requests
from social_core.backends.google import GoogleOAuth2
from google.auth.transport import requests
from django.conf import settings
from rest_framework import views, status
from rest_framework.response import Response
from social_django.utils import psa
from django.views import View
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class Register(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            user = User.objects.get(name = serializer.data['name'])
            refresh = RefreshToken.for_user(user)
            return Response( {'id':str(user.id),'refresh': str(refresh),'access': str(refresh.access_token),'message':"Register successfully"},status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def join_create(request):
    serializer = JoinSerializer(data=request.data)
    if serializer.is_valid():
        join_instance = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.contrib.auth import authenticate, login

'''
@method_decorator(csrf_exempt, name='dispatch')
class Login(APIView):
    # serializer_class = LoginSerializer
    def post(self, request):
        email = request.data.get('email')
        
        user = authenticate(email=email)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response( {'user':str(email.id),'refresh': str(refresh),'access': str(refresh.access_token),'message':"login successfully"})
        return response.Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)
 '''

    
class User_Post(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        post = Post.objects.all()
        serializer = User_Post_serializer(post , many = True)
        return Response(serializer.data) 
         
    def post(self, request,*args, **kwargs):
        file_serializer = User_Post_serializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST','GET'])
def Create_Post(request,id):
    user = request.user
    posts = Stream.object.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.object.filter(id_in=group_ids).all().order_by('posted')
    context = {
        'post_items':post_items
    }
    
    return response(request,context.data)



#@api_view(['GET'])
class ProfileAPIView(APIView):
    
    def get(self,request):
        profile = Profile.objects.all()
        serializer = ProfileSerializer12(profile , many = True)
        return Response(serializer.data) 
    def post(self, request,*args, **kwargs):
        file_serializer = ProfileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST','GET'])
def Followers_Post(request,id):
    post = Post.objects.filter(id = id)
    if request.user in post[0].Followers_by.all():
       post[0].Followers_by.remove(request.user)
    else:
        post[0].Followers_by.add(request.user)
    return response.Response(status=status.HTTP_202_ACCEPTED) 

@csrf_exempt
@api_view(['POST','GET'])
def Following_Post(request,id):
    post = Post.objects.filter(id = id)
    if request.user in post[0].following_by.all():
       post[0].following_by.remove(request.user)
    else:
        post[0].following_by.add(request.user)
    return response.Response(status=status.HTTP_202_ACCEPTED) 

class FollowerCountView(APIView):
    def get(self, request, user_id):
        follower_count = Follow.objects.filter(following_id=user_id).count()
        return Response({'follower_count': follower_count})

class FollowingAndPostCountView(APIView):
    def get(self, request, user_id):
        following_count = Stream.objects.filter(user_id=user_id).count()
        follower_count = Stream.objects.filter(following_id=user_id).count()
        post_count = Stream.objects.filter(user_id=user_id, post__isnull=False).count()
        return Response({'following_count': following_count, 'post_count': post_count ,'follower_count': follower_count})



'''@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser,FormParser,MultiPartParser])
def login_view(request):
    if request.method =='POST':
        phone =request.POST.get('phone')
        user = User.objects.get(phone=phone)
        # if not user.exists():
        #     return response.Response(status=status.HTTP_400_BAD_REQUEST)
        
        print(user)
        user.otp = random.randint(1000,9999)
        print(user.otp)
        user.save()
        #    send_otp_on_phone(mobile,user.otp)

        return Response({'uid': str(user.uid),'OTP': int(user.otp),'message':"Otp send successfully"})
    return response.Response(status=status.HTTP_400_BAD_REQUEST)'''


@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser,FormParser,MultiPartParser])
def login_view(request):
    if request.method =='POST':
        phone =request.POST.get('phone')
        user = User.objects.get(phone=phone)
        # if not user.exists():
        #     return response.Response(status=status.HTTP_400_BAD_REQUEST)
        
        print(user)
        user.otp = random.randint(100000,999999)
        print(user.otp)
        user.save()
        # send_otp_on_phone(phone,user.otp)

        return Response({'uid': str(user.uid),'OPT': int(user.otp),'message':"Otp send successfully"})
    return response.Response(status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser,FormParser,MultiPartParser])
def otp(request,uid):
    if request.method =='POST':
        otp = request.POST.get('otp')
        print(otp)
        profile = User.objects.get(uid=uid)
        print(profile)
        if otp == profile.otp:
            print(profile.otp)
            login(request,profile)
            refresh = RefreshToken.for_user(profile)
            return Response({'user': profile.email,'id':str(profile.id),'refresh': str(refresh),'access': str(refresh.access_token),'message':"Login successfully"})

    return response.Response(status=status.HTTP_400_BAD_REQUEST)





from django.http import JsonResponse, HttpResponse


@method_decorator(csrf_exempt, name='dispatch')

class LoginAPIView(views.APIView):
    @psa()
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user against Google
        user = request.backends.google.GoogleOAuth2(email=email, password=password)
        

        if user is not None and user.is_active:
            # Login the user
            login(request, user)
            return JsonResponse({'message': 'Login successful'})  (status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
'''class LoginAPIView(View):
    @psa()
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user against Google
        backend = GoogleOAuth2()
        user = backend.auth_complete(request, {'password': password, 'email': email}, None)

        if user is not None and user.is_active:
            # Login the user
            login(request, user)
            return HttpResponse({'message': 'Login successful'})
        else:
            return HttpResponse('Invalid credentials', status=401)'''
# Create your views here.
'''@csrf_exempt
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
       serializer = UserLoginSerializer(data=request.data)
       if serializer.is_valid():
           cd=serializer.cleaned_data
           user = authenticate(request,email=cd['email'],password =cd['password'])

           if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated''successfully')
                else:
                    return HttpResponse('Disabled Account')
           else:
               return HttpResponse('invalid login')
    else:
        serializer = UserLoginSerializer()
    return response(serializer.data)'''

'''from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import parser_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse
import json

class LoginView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    @csrf_exempt
    def post(self, request):
        account_data = request.data
        account = User(**account_data)
        account.password = account.email
        existing_account = User.objects.filter(email=account.email).exists()

        if existing_account:
            response_data = {
                'message': 'You are successfully logged in',
                'token': encode(existing_account.id),
            }
            return JsonResponse(response_data, status=201)
        else:
            if account.save():
                response_data = {
                    'token': encode(account.id),
                }
                return JsonResponse(response_data, status=201)
            else:
                error_data = {
                    'errors': account.errors,
                }
                return JsonResponse(error_data, status=422)

    def get(self, request):
        error_data = {
            'errors': [
                {'account': 'Invalid account type'},
            ]
        }
        return JsonResponse(error_data, status=422)'''

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth.registration.views import SocialLoginView
from django.shortcuts import redirect



def facebook_login(request):
    app_id = '1244721809751183'
    redirect_uri = 'dashboaed'
    scope = 'email'  # Request additional permissions if needed
    facebook_login_url = f'https://www.facebook.com/v13.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope={scope}'
    return redirect(facebook_login_url)


def facebook_login_callback(request):
    app_id = '1244721809751183'
    app_secret = 'ecf2f4803c4038870663baa2ca4fdd5b'
    redirect_uri = 'dashboaed'
    code = request.GET.get('code')
    access_token_url = f'https://graph.facebook.com/v13.0/oauth/access_token?client_id={app_id}&redirect_uri={redirect_uri}&client_secret={app_secret}&code={code}'
    response = requests.get(access_token_url)
    data = response.json()
    access_token = data.get('access_token')
    # Use the access token to make API calls on behalf of the user
    # You can store the token in the user's session or use it immediately
    return HttpResponse('Successfully logged in with Facebook!')