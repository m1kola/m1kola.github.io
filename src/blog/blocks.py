from wagtail.wagtailcore import blocks as core_blocks
from wagtail.wagtaildocs import blocks as docs_blocks

from base import blocks as base_blocks


class BlogStreamBlock(core_blocks.StreamBlock):
    rich_text = core_blocks.RichTextBlock(icon='edit')
    document = docs_blocks.DocumentChooserBlock(icon='doc-full-inverse')
    code = base_blocks.CodeBlock()
    html = core_blocks.RawHTMLBlock()
