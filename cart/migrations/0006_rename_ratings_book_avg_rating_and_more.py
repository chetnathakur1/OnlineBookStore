# Generated by Django 4.2.5 on 2023-10-11 09:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_book_ratings_book_ratings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='ratings',
            new_name='avg_rating',
        ),
        migrations.AlterUniqueTogether(
            name='bookrating',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='bookrating',
            name='ratings',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
