from django.db import models


class BaseFields(models.Model):
    subtitle = models.CharField(max_length=256, blank=True)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        abstract = True
