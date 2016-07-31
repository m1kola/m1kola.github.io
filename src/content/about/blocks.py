from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailcore import blocks

from base.blocks import StoryBlock


class AboutBlock(StoryBlock):
    position_item = blocks.ListBlock(
        blocks.StructBlock([
            ('company_name', blocks.CharBlock()),
            ('position', blocks.CharBlock()),
            ('start_at', blocks.DateBlock()),
            ('leave_at', blocks.DateBlock(required=False)),
            ('location', blocks.CharBlock(required=False)),
            ('website', blocks.CharBlock(required=False)),
            ('responsibilities', blocks.RichTextBlock(required=False)),
            ('achievements', blocks.RichTextBlock(required=False)),
        ], label=_("Accordion item"), icon="doc-full"),
        icon="doc-full", template="about/blocks/position_item_block.html"
    )
