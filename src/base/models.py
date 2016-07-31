from django.db import models
from wagtail.wagtailadmin import edit_handlers
from wagtail.wagtailimages import edit_handlers as image_edit_handlers


class BaseFields(models.Model):
    subtitle = models.CharField(max_length=256, blank=True)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = [
        edit_handlers.FieldPanel('subtitle', classname='full'),
        image_edit_handlers.ImageChooserPanel('main_image'),
    ]

    class Meta:
        abstract = True
