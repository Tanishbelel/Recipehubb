# Generated by Django 5.0.6 on 2024-12-20 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veggie', '0003_recipe_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
