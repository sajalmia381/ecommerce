# Generated by Django 2.0.5 on 2018-06-09 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20180527_1210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'get_latest_by': ['-posted_on']},
        ),
    ]
