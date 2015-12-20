from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from blog.models import BlogPage, BlogIndexPage


# BlogPage

BlogPage.content_panels = Page.content_panels + [
    FieldPanel('subtitle', classname='full'),
    ImageChooserPanel('main_image'),
    FieldPanel('lead', classname='full'),
    FieldPanel('body', classname='full'),
]

BlogPage.promote_panels = Page.promote_panels + [
    FieldPanel('tags'),
]

BlogPage.parent_page_types = [
    BlogIndexPage,
]
BlogPage.subpage_types = []


# BlogIndexPage

BlogIndexPage.content_panels = Page.content_panels + [
    FieldPanel('subtitle', classname='full'),
    ImageChooserPanel('main_image'),
]

BlogIndexPage.subpage_types = [
    BlogPage,
]