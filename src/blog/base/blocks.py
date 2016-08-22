from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock


class StoryBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    embed = EmbedBlock()
