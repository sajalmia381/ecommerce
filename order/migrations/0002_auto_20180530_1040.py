# Generated by Django 2.0.5 on 2018-05-30 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_auto_20180528_2349'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Oder',
            new_name='Order',
        ),
    ]
