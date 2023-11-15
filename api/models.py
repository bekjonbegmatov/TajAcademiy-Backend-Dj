from django.db import models

class UserForm(models.Model):

    email = models.EmailField(max_length=254)
    last_name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50 , blank=True)
    password = models.CharField(max_length=50)
    sesion_tocen = models.CharField(max_length=50 , blank=True)
    score = models.IntegerField(default=100)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = ("UserForm")
        verbose_name_plural = ("UserForms")

    def __str__(self):
        return self.email

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

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("CoursesModel")
        verbose_name_plural = ("CoursesModels")

    def __str__(self):
        return self.title

class CoursDetailesListModel(models.Model):

    title = models.CharField(max_length=50)
    for_cours = models.ForeignKey(CoursesModel , verbose_name=(""), on_delete=models.CASCADE)
    number = models.IntegerField()
    description = models.TextField()
    wideo_url = models.CharField(max_length=150)

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
    created = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("UserCoursesModel_detail", kwargs={"pk": self.pk})

class UserProgress (models.Model):
    user = models.ForeignKey( UserForm , verbose_name=(""), on_delete=models.CASCADE)
    course = models.ForeignKey( CoursesModel , verbose_name=(""), on_delete=models.CASCADE) 
    finish_progres = models.IntegerField(default=10 , blank=True)
    progress = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f"{self.user} -> {self.course}"

class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to ='media/blog/images' , height_field=None, width_field=None, max_length=None)
    url = models.CharField( max_length=100 , blank=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.title

class CommentsModel(models.Model):
    user = models.ForeignKey( UserForm , verbose_name=(""), on_delete=models.CASCADE)
    course_id = models.ForeignKey(CoursDetailesListModel, verbose_name=(""), on_delete=models.CASCADE)
    test = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("CommentsModel_detail", kwargs={"pk": self.pk})

class ReviewsModel(models.Model):
    full_name = models.CharField(max_length=50)
    to_cource = models.CharField(max_length=50)
    text = models.TextField()

    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    