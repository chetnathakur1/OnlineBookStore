# Generated by Django 4.2.5 on 2023-09-28 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_alter_orderitem_book_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]