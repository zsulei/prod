# Generated by Django 5.0.2 on 2024-04-12 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_picture_product_product_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Picture',
            new_name='Image',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='picture',
            new_name='image',
        ),
    ]
