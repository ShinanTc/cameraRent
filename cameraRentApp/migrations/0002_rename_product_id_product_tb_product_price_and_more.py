# Generated by Django 4.0.1 on 2022-02-08 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cameraRentApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_tb',
            old_name='product_id',
            new_name='product_price',
        ),
        migrations.RemoveField(
            model_name='seller_tb',
            name='seller_id',
        ),
        migrations.RemoveField(
            model_name='user_tb',
            name='booking_id',
        ),
        migrations.AddField(
            model_name='product_tb',
            name='product_description',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.DeleteModel(
            name='book_tb',
        ),
    ]