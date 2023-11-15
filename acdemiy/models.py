from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class UserForm(models.Model):
    user = models.ForeignKey( User , verbose_name=(""), on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    last_name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50 , blank=True)
    password = models.CharField(max_length=50)
    score = models.IntegerField(blank=True , default=100)

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