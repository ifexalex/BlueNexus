# Generated by Django 3.2.9 on 2021-11-17 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20211117_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_eligible',
            field=models.BooleanField(default=False, help_text='Designates whether the user can is eligible for credit purchase.', verbose_name='Eligible for Credit purchase'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, verbose_name='phone number'),
        ),
    ]
