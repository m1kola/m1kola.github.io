from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin import edit_handlers
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailimages import edit_handlers as image_edit_handlers


class BaseFields(models.Model):
    subtitle = models.CharField(max_length=256, blank=True)
    main_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='+')
    share_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='+')

    promote_panels = [
        MultiFieldPanel([
            edit_handlers.FieldPanel('subtitle'),
            image_edit_handlers.ImageChooserPanel('main_image'),
        ], heading=_("Header")),
        MultiFieldPanel([
            image_edit_handlers.ImageChooserPanel('share_image'),
        ], heading=_("Social media fields")),
    ]

    class Meta:
        abstract = True
