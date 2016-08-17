# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailimages.formats import Format, register_image_format, unregister_image_format

unregister_image_format('fullwidth')
register_image_format(Format('fullwidth', _("Full width"), 'richtext-image full-width img-responsive', 'width-800'))

unregister_image_format('left')
register_image_format(Format('left', _("Left-aligned"), 'richtext-image left img-responsive', 'width-500'))

unregister_image_format('right')
register_image_format(Format('right', _("Right-aligned"), 'richtext-image right img-responsive', 'width-500'))
