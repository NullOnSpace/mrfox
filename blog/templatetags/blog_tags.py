from django.utils.safestring import mark_safe
from django.template import Library

import markdown


register = Library()


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
