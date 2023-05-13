from django import template

register = template.Library()

@register.filter
def enumerate_list(lst):
    return list(enumerate(lst))