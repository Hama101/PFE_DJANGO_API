# Generated by Django 4.0.2 on 2022-03-02 15:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_recipe_images_alter_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 2, 11, 31, 7, 739721)),
        ),
    ]
