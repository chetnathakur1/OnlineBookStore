# Generated by Django 4.2.5 on 2023-09-25 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_books'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=12)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.RenameModel(
            old_name='Books',
            new_name='Book',
        ),
        migrations.AddField(
            model_name='cart',
            name='books',
            field=models.ManyToManyField(to='cart.book'),
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.customer'),
        ),
    ]
