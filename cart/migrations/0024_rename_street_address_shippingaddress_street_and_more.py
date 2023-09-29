# Generated by Django 4.2.5 on 2023-09-29 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0023_remove_shippingaddress_order_order_shipping_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='street_address',
            new_name='street',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.order'),
        ),
    ]