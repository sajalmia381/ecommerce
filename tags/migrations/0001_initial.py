# Generated by Django 2.0.5 on 2018-05-27 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0010_auto_20180527_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField()),
                ('active', models.BooleanField(default=True)),
                ('products', models.ManyToManyField(blank=True, to='product.Product')),
            ],
        ),
    ]
