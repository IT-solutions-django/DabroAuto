from django import template

register = template.Library()


@register.filter
def beautify_number(value):
    return "{0:,}".format(int(value)).replace(",", " ")


@register.filter
def range_filter(value):
    return range(value)


@register.filter
def round_price(value):
    return int(value) // 1000 * 1000


@register.filter
def beautify_url(value):
    return str(value).lower().replace(" ", "")


@register.filter
def multiply(value, arg):
    return float(value) * float(arg)


@register.filter
def float_normalize(value):
    return str(value).replace(",", ".")


@register.filter
def percentage(value, perc):
    return float(value) / 100 * perc
