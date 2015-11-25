from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name
from wagtail.wagtailcore import blocks


class CodeBlock(blocks.StructBlock):
    """
    Code Highlighting Block
    """
    LANGUAGE_CHOICES = (
        ('python', 'Python'),
        ('php', 'PHP'),
        ('bash', 'Bash/Shell'),
        ('html', 'HTML'),
        ('js', 'JavaScript'),
        ('css', 'CSS'),
        ('scss', 'SCSS'),
    )

    language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES, required=False)
    code = blocks.TextBlock()

    class Meta:
        icon = 'code'

    def render(self, value):
        src = value['code'].strip('\n')
        lang = value['language']

        print lang
        lexer = get_lexer_by_name(lang)
        formatter = get_formatter_by_name(
            'html',
            linenos=None,
            noclasses=False,
        )
        return mark_safe(highlight(src, lexer, formatter))
