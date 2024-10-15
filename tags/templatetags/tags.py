from django import template

register = template.Library()


@register.filter
def beautify_number(value):
    return "{0:,}".format(int(value)).replace(",", " ")
