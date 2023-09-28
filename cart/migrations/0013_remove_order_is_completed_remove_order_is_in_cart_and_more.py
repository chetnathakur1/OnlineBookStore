# Generated by Django 4.2.5 on 2023-09-28 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_order_is_in_cart_alter_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_completed',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_in_cart',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('cart', 'Cart'), ('completed', 'Completed')], default='cart', max_length=20),
        ),
    ]
