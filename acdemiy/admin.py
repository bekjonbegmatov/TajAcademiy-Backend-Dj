from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.UserForm)
admin.site.register(models.Blog)
admin.site.register(models.CommentsModel)
admin.site.register(models.UserTest)
admin.site.register(models.CoursesModel)
admin.site.register(models.CoursesCategory)
admin.site.register(models.CoursDetailesListModel)
admin.site.register(models.UserCoursesModel)
admin.site.register(models.Forum_Model)
admin.site.register(models.Comments_Forum_Model)
