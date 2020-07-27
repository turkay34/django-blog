# Generated by Django 3.0.8 on 2020-07-24 12:34

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200724_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(blank=True, default='Anonim', max_length=50, null=True, verbose_name='İsim')),
                ('soyisim', models.CharField(blank=True, max_length=50, null=True, verbose_name='Soyisim')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('yorum', ckeditor.fields.RichTextField(help_text='Yorumunuzu yazınız...', max_length=500, null=True, verbose_name='Yorum')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.makale')),
            ],
        ),
    ]
