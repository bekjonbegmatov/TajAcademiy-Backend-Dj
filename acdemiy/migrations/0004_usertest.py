# Generated by Django 4.2.7 on 2023-11-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acdemiy', '0003_commentsmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('test1', models.CharField(max_length=50)),
                ('test2', models.CharField(max_length=50)),
                ('test3', models.CharField(max_length=50)),
                ('correct_ansver', models.CharField(max_length=50)),
            ],
        ),
    ]
