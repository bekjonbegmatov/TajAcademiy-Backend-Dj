# Generated by Django 4.2.7 on 2023-11-16 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acdemiy', '0010_alter_usercoursesmodel_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercoursesmodel',
            name='last_curs_id',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]