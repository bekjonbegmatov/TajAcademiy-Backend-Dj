from django.urls import path
from . import  views
# import set
app_name = "academiy"
urlpatterns = [
    path('' , views.index , name='main'),                  # Main pagge

    #------- AUTH PATHS ---------#
    path('login' , views.login , name='login'),
    path('logout' , views.logout , name='logout'),
    path('register' , views.register , name='register'),

    path('profile' , views.profile , name='profile'),      # User Progile

    path('blog' , views.blog , name='blog'),               # Blog
    path('detail/<int:pk>/' , views.blog_detail , name='detail'),
    path('create/comment' , views.create_comment , name='create_comment')
]
