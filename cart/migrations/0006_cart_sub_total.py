# Generated by Django 2.0.5 on 2018-05-28 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20180528_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
    ]
