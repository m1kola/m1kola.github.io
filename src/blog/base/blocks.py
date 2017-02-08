from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name
from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock


class CodeBlock(blocks.StructBlock):
    """
    Code Highlighting Block
    """

    DEFAULT_LANG = 'bash'

    LANGUAGE_CHOICES = (
        ('python', _("Python")),
        ('php', _("PHP")),
        ('bash', _("Bash/Shell")),
        ('html', _("HTML")),
        ('js', _("JavaScript")),
        ('django', _("Django templating language")),
        ('css', _("CSS")),
        ('scss', _("SCSS")),
    )

    language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES, required=False)
    code = blocks.TextBlock()

    class Meta:
        icon = 'code'
        template = 'base/blocks/code_block.html'

    def get_context(self, value, parent_context=None):
        src = value.get('code', '').strip('\n')
        lang = value.get('language') or self.DEFAULT_LANG

        lexer = get_lexer_by_name(lang)
        formatter = get_formatter_by_name('html', linenos=None, noclasses=False)

        context = super().get_context(value, parent_context)
        context.update({
            'highlighted_value': mark_safe(highlight(src, lexer, formatter)),
        })

        return context


class StoryBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    embed = EmbedBlock()
    code = CodeBlock()
