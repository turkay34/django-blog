# Generated by Django 3.0.8 on 2020-07-20 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_kategori'),
    ]

    operations = [
        migrations.AddField(
            model_name='makale',
            name='kategori',
            field=models.ManyToManyField(null=True, to='blog.kategori'),
        ),
    ]
