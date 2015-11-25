# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import modelcluster.contrib.taggit
import wagtail.wagtaildocs.blocks
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.CharField(max_length=256, blank=True)),
                ('main_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subtitle', models.CharField(max_length=256, blank=True)),
                ('body', wagtail.wagtailcore.fields.StreamField([(b'rich_text', wagtail.wagtailcore.blocks.RichTextBlock(icon=b'edit')), (b'document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon=b'doc-full-inverse')), (b'code', wagtail.wagtailcore.blocks.StructBlock([(b'language', wagtail.wagtailcore.blocks.ChoiceBlock(required=False, choices=[(b'python', b'Python'), (b'php', b'PHP'), (b'bash', b'Bash/Shell'), (b'html', b'HTML'), (b'js', b'JavaScript'), (b'css', b'CSS'), (b'scss', b'SCSS')])), (b'code', wagtail.wagtailcore.blocks.TextBlock())])), (b'html', wagtail.wagtailcore.blocks.RawHTMLBlock())])),
                ('lead', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('main_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', modelcluster.fields.ParentalKey(related_name='tagged_items', to='blog.BlogPage')),
                ('tag', models.ForeignKey(related_name='blog_blogpagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='blogpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(to='taggit.Tag', through='blog.BlogPageTag', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
