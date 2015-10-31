from django.conf import settings as global_settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.functional import cached_property

from . import settings


class TagMeta(models.Model):
    slug = models.CharField(primary_key=True,
                            max_length=64,
                            unique=True,
                            validators=[
                                RegexValidator(
                                    r'^%s$' % settings.TAG_SLUG_REGEX,
                                )
                            ])

    def __unicode__(self):
        return self.slug


class Tag(models.Model):
    tag_meta = models.ForeignKey(TagMeta, related_name='tags_set')
    language_code = models.CharField(max_length=7, choices=global_settings.LANGUAGES)
    title = models.CharField(max_length=256)

    @cached_property
    def slug(self):
        return self.tag_meta.slug

    def __unicode__(self):
        return self.title

    class Meta(object):
        unique_together = ('tag_meta', 'language_code')


class PostMeta(models.Model):
    slug = models.CharField(primary_key=True,
                            max_length=64,
                            unique=True,
                            validators=[
                                RegexValidator(
                                    r'^%s$' % settings.POST_SLUG_REGEX,
                                )
                            ])

    image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    tags = models.ManyToManyField(TagMeta, related_name='tagsmetas_set', blank=True)

    def __unicode__(self):
        return self.slug


class Post(models.Model):
    post_meta = models.ForeignKey(PostMeta, related_name='posts_set')
    language_code = models.CharField(max_length=7, choices=global_settings.LANGUAGES)

    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=256, blank=True)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @cached_property
    def slug(self):
        return self.post_meta.slug
    slug.admin_order_field = 'post__slug'

    @cached_property
    def image(self):
        return self.post_meta.image

    @cached_property
    def tags(self):
        # TODO: Review needed
        return self.post_meta.tags

    def __unicode__(self):
        return self.title

    class Meta(object):
        unique_together = ('post_meta', 'language_code')

