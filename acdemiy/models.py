from django.db import models
from django.contrib.auth.models import User 
from  embed_video.fields  import  EmbedVideoField

# Create your models here.
class UserForm(models.Model):
    user = models.ForeignKey( User , verbose_name=(""), on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    last_name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50 , blank=True)
    password = models.CharField(max_length=50)
    score = models.IntegerField(blank=True , default=0)

    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = ("UserForm")
        verbose_name_plural = ("UserForms")

    def __str__(self):
        return self.email

class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250  , blank=True)
    full_text = models.TextField()
    image = models.ImageField(upload_to ='media/blog/images' , height_field=None, width_field=None, max_length=None)
    url = models.CharField( max_length=100 , blank=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.title

class CommentsModel(models.Model):
    user = models.ForeignKey( UserForm , verbose_name=(""), on_delete=models.CASCADE)
    course_id = models.ForeignKey(Blog, verbose_name=(""), on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created)

    def get_absolute_url(self):
        return reverse("CommentsModel_detail", kwargs={"pk": self.pk})

class UserTest(models.Model):

    title = models.CharField(max_length=250)

    test1 = models.CharField(max_length=50)
    test2 = models.CharField(max_length=50)
    test3 = models.CharField(max_length=50)

    correct_ansver = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class CoursesCategory(models.Model):
    categoty = models.CharField(max_length=50)
    def __str__(self):
        return self.categoty

class CoursesModel(models.Model):

    title = models.CharField(max_length=50)
    category = models.ForeignKey(CoursesCategory, verbose_name=(""), on_delete=models.CASCADE)
    desriptions = models.TextField()
    image = models.ImageField(upload_to='media/courses/image', height_field=None, width_field=None, max_length=None)
    languages = models.CharField(max_length=200)
    score = models.IntegerField(default=0 , blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("CoursesModel")
        verbose_name_plural = ("CoursesModels")

    def __str__(self):
        return self.title

class CoursDetailesListModel(models.Model):

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/courses_detail/image', height_field=None, width_field=None, max_length=None , blank=True)
    for_cours = models.ForeignKey(CoursesModel , verbose_name=(""), on_delete=models.CASCADE)
    number = models.IntegerField()
    description = models.TextField()
    video = EmbedVideoField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("CoursDetailesListModel")
        verbose_name_plural = ("CoursDetailesListModels")

    def __str__(self):
        return self.title

class UserCoursesModel(models.Model):

    user = models.ForeignKey( UserForm , verbose_name=(""), on_delete=models.CASCADE)
    course = models.ForeignKey( CoursesModel , verbose_name=(""), on_delete=models.CASCADE) 
    score = models.IntegerField(default=1)
    last_curs_id = models.IntegerField(default=1 , blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username

    def get_absolute_url(self):
        return reverse("UserCoursesModel_detail", kwargs={"pk": self.pk})
    
class Forum_Model(models.Model):
    title = models.CharField(max_length=100)
    full_text = models.TextField()
    url = models.CharField( max_length=100 , blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

class Comments_Forum_Model(models.Model):
    user = models.ForeignKey( UserForm , verbose_name=(""), on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum_Model, verbose_name=(""), on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created)

    def get_absolute_url(self):
        return reverse("CommentsModel_detail", kwargs={"pk": self.pk})