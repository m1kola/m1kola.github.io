# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=7, choices=[(b'en', b'English'), (b'ru', b'Russian')])),
                ('title', models.CharField(max_length=256)),
                ('subtitle', models.CharField(max_length=256, blank=True)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostMeta',
            fields=[
                ('slug', models.CharField(max_length=64, unique=True, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(b'^[a-z0-9-]+$')])),
                ('image', models.ImageField(upload_to=b'blog/images/%Y/%m/%d', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=7, choices=[(b'en', b'English'), (b'ru', b'Russian')])),
                ('title', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='TagMeta',
            fields=[
                ('slug', models.CharField(max_length=64, unique=True, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(b'^[a-z-]+$')])),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='tag_meta',
            field=models.ForeignKey(related_name='tags_set', to='blog.TagMeta'),
        ),
        migrations.AddField(
            model_name='postmeta',
            name='tags',
            field=models.ManyToManyField(related_name='tagsmetas_set', to='blog.TagMeta', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_meta',
            field=models.ForeignKey(related_name='posts_set', to='blog.PostMeta'),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('tag_meta', 'language_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('post_meta', 'language_code')]),
        ),
    ]
