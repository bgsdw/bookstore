# Generated by Django 4.0.4 on 2022-05-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_author_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='Created_Time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='Is_Disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='Created_Time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='Created_Time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
