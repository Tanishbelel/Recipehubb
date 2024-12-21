# Generated by Django 5.0.6 on 2024-12-21 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veggie', '0006_remove_recipe_favorites_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('icon', models.ImageField(upload_to='category_icons/')),
            ],
        ),
    ]