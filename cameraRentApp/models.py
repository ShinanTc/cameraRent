from distutils.command.upload import upload
from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.forms import DateField

# Create your models here.


class user_tb(models.Model):
    buyer_name = models.CharField(max_length=100, default='')
    user_name = models.CharField(max_length=100, default='')
    user_email = models.CharField(max_length=100, default='')
    user_password = models.CharField(max_length=32, default='')
    user_phone = models.CharField(max_length=32, default='')


class seller_tb(models.Model):
    seller_name = models.CharField(max_length=100, default='')
    user_name = models.CharField(max_length=100, default='')
    user_email = models.CharField(max_length=100, default='')
    user_password = models.CharField(max_length=32, default='')
    status = models.CharField(max_length=32, default='pending')


class product_tb(models.Model):
    seller_id = models.ForeignKey(seller_tb, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, default='')
    product_price = models.CharField(max_length=32, default='')
    product_description = models.CharField(max_length=100, default='')
    product_img = models.ImageField(upload_to='images', default='')


class book_tb(models.Model):
    user_id = models.ForeignKey(user_tb, on_delete=models.CASCADE, default='')
    product_id = models.ForeignKey(
        product_tb, on_delete=models.CASCADE, default='')
    seller_id = models.ForeignKey(
        seller_tb, on_delete=models.CASCADE, default='')
    book_from = models.DateField(max_length=100, default='')
    book_to = models.DateField(max_length=100, default='')
