# Generated by Django 3.0.8 on 2020-07-27 08:26

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20200724_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='yorum',
            field=ckeditor.fields.RichTextField(default='Default yorum', help_text='Yorumunuzu yazınız...', max_length=500, null=True, verbose_name='Yorum'),
        ),
    ]
