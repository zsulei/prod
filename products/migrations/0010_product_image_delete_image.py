# Generated by Django 5.0.2 on 2024-04-17 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_product_image_image_product_alter_image_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
