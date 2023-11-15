from django.shortcuts import render , redirect
from django.http import HttpResponse 
# Create your views here.
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm 
from django.contrib.auth.models import User 
from django.db import IntegrityError
from django.contrib.auth import logout , authenticate 
from django.contrib.auth import login as auth_login

from . import models as db

# ------------- CODE -------------#

def index(request):
    return render(request=request , template_name='academiy/index.html')


# --------- USER AUTH AND REGISTER --------------#
def login(request):
    if request.method == 'GET': return render(request , 'academiy/login.html' , {'form' : AuthenticationForm()})
    else :
        user = authenticate(request=request , username=request.POST['username'] , password=request.POST['password'])
        if user is not None :
            auth_login(request , user)
            return redirect('academiy:main')
        return render(request, 'academiy/login.html', {'form' : AuthenticationForm() , 'error' : 'Имя ползователья или парол не совпвдвет'})
        

def register(request):
    if request.method == "GET" : return render(request , 'academiy/register.html' , {'form' : UserCreationForm()})
    else :
        if request.POST['username'] == '' or len(request.POST['username']) < 5 : return render(request , 'academiy/register.html' , {'form' : UserCreationForm() , 'error' : "Длина ползователя должен быт минимум 5 символов"})
        elif len(request.POST['password1']) <= 8 or len(request.POST['password2']) <= 8 : return render(request , 'academiy/register.html' , {'form' : UserCreationForm() , 'error' : "Парол должен не мене 8 символов"})
        elif len(request.POST['email']) == 0 : return render(request , 'academiy/register.html' , {'form' : UserCreationForm() , 'error' : "Ведите свой email"})
        elif request.POST['password1'] == request.POST['password2']:
            try :
                user = User.objects.create_user(username=request.POST['username'] , password=request.POST['password1'])
                user.save()
                user_info = db.UserForm(user=user , email=request.POST['email'] , password=request.POST['password1'])
                user_info.save()
                auth_login(request , user)
                return redirect('academiy:main')

            except IntegrityError : return render(request , 'academiy/register.html' , {'form' : UserCreationForm() , 'error' : "Ой это имя уже занета"})
        return render(request, 'academiy/register.html' , {'form' : UserCreationForm() , 'error' : 'Пароли не совпадають'})

def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('academiy:main')

# ------------- USER PROFILR ---------------#
def profile(request):
    if request.user.is_authenticated : return render(request , 'academiy/profile.html')
    else : return render(request , 'academiy/register.html' , {'form' : UserCreationForm()})

# ----------- BLOG -----------------------#
def blog(request):
    blogs = db.Blog.objects.order_by('-created')
    return render(request , 'academiy/blog.html' , {'blogs' : blogs})

def blog_detail(request , pk):
    blog = db.Blog.objects.get(id=pk)
    coments = db.CommentsModel.objects.filter(course_id=pk)
    return render(request , 'academiy/blog_detail.html' , {'blog' : blog , 'coments' : coments})

def create_comment(request):
    user = request.user
    us_form = db.UserForm.objects.get(user=user)
    blog_id = request.POST['blog_id']
    blog = db.Blog.objects.get(id=blog_id)
    try :
        coment = db.CommentsModel(user=us_form, course_id=blog , text=request.POST['comment'])
        coment.save()
        blog = db.Blog.objects.get(id=blog_id)
        coments = db.CommentsModel.objects.filter(course_id=blog_id)
        return render(request , 'academiy/blog_detail.html' , {'blog' : blog , 'coments' : coments})
    except IntegrityError:
        return redirect('academiy:blog')

