# Generated by Django 5.0.6 on 2024-06-16 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_cartitem_quantity_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
