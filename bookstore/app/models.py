from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.

class Author(models.Model):
    Author_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Pen_Name = models.CharField(max_length=255)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=255, validators=[MinLengthValidator(8)])
    Is_Disabled = models.BooleanField(default=False)
    Created_Time = models.DateTimeField(auto_now_add=True)

class Book(models.Model):
    Book_ID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Author_ID = models.ForeignKey(Author, on_delete=models.RESTRICT)
    Summary = models.CharField(max_length=255)
    Stock = models.PositiveIntegerField()
    Price = models.PositiveIntegerField()
    Cover_URL = models.ImageField(upload_to='bookstore/app/uploads/')
    Created_Time = models.DateTimeField(auto_now_add=True)

class Sales(models.Model):
    Sales_ID = models.AutoField(primary_key=True)
    Recepient_Name = models.CharField(max_length=255)
    Recepient_Email = models.CharField(max_length=255)
    Book_Title = models.CharField(max_length=255)
    Author_ID = models.ForeignKey(Author, on_delete=models.RESTRICT)
    Quantity = models.PositiveIntegerField()
    Price_Per_Unit = models.PositiveIntegerField()
    Price_Total = models.PositiveIntegerField()
    Created_Time = models.DateTimeField(auto_now_add=True)
