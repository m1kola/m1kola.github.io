from wagtail.wagtailadmin import edit_handlers
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages import edit_handlers as image_edit_handlers

from blog.models import BlogPage, BlogIndexPage


# BlogPage

BlogPage.content_panels = Page.content_panels + [
    edit_handlers.FieldPanel('subtitle', classname='full'),
    image_edit_handlers.ImageChooserPanel('main_image'),
    edit_handlers.FieldPanel('lead', classname='full'),
    edit_handlers.FieldPanel('body', classname='full'),
]

BlogPage.promote_panels = Page.promote_panels + [
    edit_handlers.FieldPanel('tags'),
]

BlogPage.parent_page_types = [
    BlogIndexPage,
]
BlogPage.subpage_types = []


# BlogIndexPage

BlogIndexPage.content_panels = Page.content_panels + [
    edit_handlers.FieldPanel('subtitle', classname='full'),
    image_edit_handlers.ImageChooserPanel('main_image'),
]

BlogIndexPage.subpage_types = [
    BlogPage,
]