# Generated by Django 5.0.2 on 2024-04-12 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_rename_picture_image_rename_picture_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='image',
            name='product',
            field=models.ManyToManyField(to='products.product'),
        ),
    ]
