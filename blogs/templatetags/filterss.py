from django import template
from urllib.parse import urlencode
register = template.Library()


@register.filter
def update_page(d, value):
    d = d.copy()
    d["page"] = value
    return d


@register.filter
def encode_params(params):
    return urlencode(params)
