from django import template
from django.urls import reverse

register = template.Library()


@register.filter(name='label_link')
def label_link(value):
    url = reverse('print-label')
    return f'{url}?shipments={value}'
