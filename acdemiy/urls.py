from django.urls import path
from . import  views

app_name = "academiy"

urlpatterns = [
    path('' , views.index , name='main'),                  # Main pagge

    #------- AUTH PATHS ---------#
    path('login' , views.login , name='login'),
    path('logout' , views.logout , name='logout'),
    path('register' , views.register , name='register'),

    path('profile' , views.profile , name='profile'),      # User Progile
    path('user/testing' , views.testing , name='testing'),
    path('user/course/add/new' , views.course_add_user , name='add_cource'),

    path('blog' , views.blog , name='blog'),               # Blog
    path('detail/<int:pk>/' , views.blog_detail , name='detail'),
    path('create/comment' , views.create_comment , name='create_comment'),
    
    #----------- Courses -------------#
    path('courses' , views.courses , name='courses'),
    path('courses/full/<int:pk>/' , views.courses_full , name='full'),
    path('courses/full/wathch/<int:pk>' , views.courses_full_watch , name='watch'),
    path('courses/full/add' , views.courses_full_watched , name='watched'),
]
