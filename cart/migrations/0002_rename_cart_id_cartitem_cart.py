# Generated by Django 3.2.9 on 2021-11-17 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='cart_id',
            new_name='cart',
        ),
    ]
