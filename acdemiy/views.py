from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
import random

from . import models as db

# ------------- CODE -------------#


def index(request):
    courses = db.CoursesModel.objects.all()
    blog = db.Blog.objects.all()
    cor = []
    blg = []
    for i in range(4):
        cor.append(random.choice(courses))
        if i > 1 : blg.append(random.choice(blog))
    context = {
        "courses": cor,
        'blogs': blg, 
    }
    return render(request=request, template_name="academiy/index.html" ,context=context)


# --------- USER AUTH AND REGISTER --------------#
def login(request):
    if request.method == "GET":
        return render(request, "academiy/login.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request=request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is not None:
            auth_login(request, user)
            return redirect("academiy:main")
        return render(
            request,
            "academiy/login.html",
            {
                "form": AuthenticationForm(),
                "error": "Имя ползователья или парол не совпвдвет",
            },
        )


def register(request):
    if request.method == "GET":
        return render(request, "academiy/register.html", {"form": UserCreationForm()})
    else:
        if request.POST["username"] == "" or len(request.POST["username"]) < 5:
            return render(
                request,
                "academiy/register.html",
                {
                    "form": UserCreationForm(),
                    "error": "Длина ползователя должен быт минимум 5 символов",
                },
            )
        elif len(request.POST["password1"]) <= 8 or len(request.POST["password2"]) <= 8:
            return render(
                request,
                "academiy/register.html",
                {
                    "form": UserCreationForm(),
                    "error": "Парол должен не мене 8 символов",
                },
            )
        elif len(request.POST["email"]) == 0:
            return render(
                request,
                "academiy/register.html",
                {"form": UserCreationForm(), "error": "Ведите свой email"},
            )
        elif request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                user_info = db.UserForm(
                    user=user,
                    email=request.POST["email"],
                    password=request.POST["password1"],
                )
                user_info.save()
                auth_login(request, user)
                return redirect("academiy:main")

            except IntegrityError:
                return render(
                    request,
                    "academiy/register.html",
                    {"form": UserCreationForm(), "error": "Ой это имя уже занета"},
                )
        return render(
            request,
            "academiy/register.html",
            {"form": UserCreationForm(), "error": "Пароли не совпадають"},
        )


def logout(request):
    auth_logout(request)
    return redirect("academiy:main")


# ------------- USER PROFILR ---------------#
def profile(request):
    if request.user.is_authenticated:
        user = db.UserForm.objects.get(user=request.user)
        user_courses = db.UserCoursesModel.objects.filter(user=user)
        user_form = db.UserForm.objects.get(user=request.user)
        user_status = "начинающий"
        if user_form.score <= 40:
            pass
        elif user_form.score <= 80:
            user_status = "средний"
        elif user_form.score <= 100:
            user_status = "Высокий"
        return render(
            request,
            "academiy/profile.html",
            {
                "user_info": user_form,
                "user_status": user_status,
                'user_courses' : user_courses
            },
        )
    else:
        return render(request, "academiy/register.html", {"form": UserCreationForm()})


# ----------- BLOG -----------------------#
def blog(request):
    blogs = db.Blog.objects.order_by("-created")
    return render(request, "academiy/blog.html", {"blogs": blogs})


def blog_detail(request, pk):
    blog = db.Blog.objects.get(id=pk)
    coments = db.CommentsModel.objects.filter(course_id=pk)
    return render(
        request, "academiy/blog_detail.html", {"blog": blog, "coments": coments}
    )

def create_comment(request):
    if request.method == ['POST'] and request.user.is_authenticated:
        user = request.user
        us_form = db.UserForm.objects.get(user=user)
        blog_id = request.POST["blog_id"]
        blog = db.Blog.objects.get(id=blog_id)
        try:
            coment = db.CommentsModel(
                user=us_form, course_id=blog, text=request.POST["comment"]
            )
            coment.save()
            blog = db.Blog.objects.get(id=blog_id)
            coments = db.CommentsModel.objects.filter(course_id=blog_id)
            return render(
                request, "academiy/blog_detail.html", {"blog": blog, "coments": coments}
            )
        except IntegrityError:
            return redirect("academiy:blog")
    return render(request , 'academiy/error.html' , {'error' : 'походу вы не зарегистрированы пожалуйста зарегистрируйте'})
    


# ----------------- TESTING --------------------#
def testing(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user_mod = db.UserForm.objects.get(user=request.user)
            user_mod.score = 0
            user_mod.save()
            test = db.UserTest.objects.get(id=1)
            return render(request, "academiy/testing.html", {"test": test})
        if request.method == "POST":
            last_id = request.POST["last_id"]
            is_end = False
            user_mod = db.UserForm.objects.get(user=request.user)
            if request.POST["ansver"] == request.POST["correct_ansver"]:
                user_mod.score += 10
                user_mod.save()
                if int(last_id) == 10:
                    corect_ansveers = user_mod.score
                    is_end = True
                    return render(
                        request,
                        "academiy/testing.html",
                        {"can": corect_ansveers, "is_end": is_end},
                    )
                test = db.UserTest.objects.get(id=int(last_id) + 1)
                return render(
                    request, "academiy/testing.html", {"test": test, "is_end": is_end}
                )
            if int(last_id) == 10:
                corect_ansveers = user_mod.score
                is_end = True
                return render(
                    request,
                    "academiy/testing.html",
                    {"can": corect_ansveers, "is_end": is_end},
                )
            test = db.UserTest.objects.get(id=int(last_id) + 1)
            return render(request, "academiy/testing.html", {"test": test})
    return render(request , 'academiy/error.html' , {'error' : 'походу вы не зарегистрированы пожалуйста зарегистрируйте'})
    


# ------------ courses ------------ #
def courses(request):
    # if request.user.is_authenticated:
    if request.method == "GET":
        catigoriyes = db.CoursesCategory.objects.all()
        courses = db.CoursesModel.objects.all()
        context = {"cat": catigoriyes, "courses": courses, "is_categoty": False}
        return render(request, "academiy/courses.html", context)
    c = request.POST["catg"]
    cat = db.CoursesCategory.objects.get(id=c)
    courses = db.CoursesModel.objects.filter(category=cat)

    context = {"cat": cat , "courses": courses, "is_categoty": True}
    return render(request, "academiy/courses.html", context)


def courses_full(request, pk):
    try:
        cours = db.CoursesModel.objects.get(id=pk)
        pod_kurses = db.CoursDetailesListModel.objects.filter(for_cours=cours)
    except:
        return HttpResponse("<h1>404 fage not found !</h1>")
    context = {"pod_curs": pod_kurses, "cours": cours}
    return render(request, "academiy/courses_full.html", context)


def courses_full_watch(request, pk):
    try:
        course = db.CoursDetailesListModel.objects.get(id=pk)
    except:
        return HttpResponse("<h1>404 fage not found !</h1>")
    context = {
        "curs": course,
    }
    return render(request, "academiy/watch_course_video.html", context)
    # return HttpResponse(f'Hello {pk}')


def course_add_user(request):
    if request.method == "POST" and request.user.is_authenticated:
        user_form = db.UserForm.objects.get(user=request.user)
        pk = request.POST["course_id"]
        cource = db.CoursesModel.objects.get(id=request.POST["course_id"])
        try :
            if db.UserCoursesModel.objects.get(user=user_form, course=cource):
                return redirect("academiy:profile")
        except:
            user_course_model = db.UserCoursesModel(user=user_form, course=cource, score=0)
            user_course_model.save()
            return redirect(f"/courses/full/{pk}/")
    return render(request , 'academiy/error.html' , {'error' : 'походу вы не зарегистрированы пожалуйста зарегистрируйте'})


def courses_full_watched(request):
    if request.method == "POST" and request.user.is_authenticated:
        pk = request.POST['cource_id']
        user = db.UserForm.objects.get(user=request.user)
        course = db.CoursesModel.objects.get(id=pk)
        idd = course.id
        uc_model = db.UserCoursesModel.objects.get(user=user , course=course)
        uc_model.score += 1
        lid = request.POST['cource_last_id']
        uc_model.last_curs_id = lid
        uc_model.save()
        return redirect(f"/courses/full/{idd}/")
    else : return render(request , 'academiy/error.html' , {'error' : 'походу вы не зарегистрированы пожалуйста зарегистрируйте'})


#  ================= FORUM =================#
def forum(request):
    forms = db.Forum_Model.objects.order_by('-created')
    context = {
        'forums' : forms,
        'is_detail' : False, 
    }
    return render(request , 'academiy/form.html' , context)

def forum_create(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request , 'academiy/form_add.html')
        title = request.POST['title']
        text = request.POST['fulltext']
        if title == '' or text == '':
            return render(request , 'academiy/form_add.html' , {'error' : 'все являются обязательными для пополнения'})
        try:
            form = db.Forum_Model(title=title , full_text=text)
            form.save()
            return redirect('academiy:forum')
        except:
            return render(request , 'academiy/form_add.html' , {'error' : 'все являются обязательными для пополнения'})
    return render(request , 'academiy/error.html' , {'error' : 'походу вы не зарегистрированы пожалуйста зарегистрируйте'})
    
def forum_detaile(request , pk):
    try:
        form = db.Forum_Model.objects.get(id=pk)
        coments = db.Comments_Forum_Model.objects.filter(forum=form)
        context = {
            'form' : form,
            'comments' : coments,
            'is_detail' : True, 
        } 
    except:
        return render(request , 'academiy/error.html' , {'error' : 'такая страница не существует 404'})

    return render(request , 'academiy/form.html' , context)

def forum_detaile_ansver(request):
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST['text']
        id_f = request.POST['form_id']
        if text == '':
            return forum_detaile(request , id_f)
        user = db.UserForm.objects.get(user=request.user)
        form = db.Forum_Model.objects.get(id=id_f)
        try :
            comment = db.Comments_Forum_Model(user=user , forum=form , text=text)
            comment.save()
            return forum_detaile(request , id_f)
        except :
            return forum_detaile(request , id_f)
    return render(request , 'academiy/error.html' , {'error' : 'походу вы не зарегистрированы пожалуйста зарегистрируйте'})