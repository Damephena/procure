# Generated by Django 3.0.7 on 2020-07-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(blank=True, default='E-HeEYJ6R9p_tTMVPFS2xYcLktC2QPZmcB82wR_IJE8', max_length=250, unique=False),
        ),
    ]
