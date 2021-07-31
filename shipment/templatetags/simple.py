from django import template
from django.urls import reverse

from thairod.services.shippop.api import ShippopAPI

register = template.Library()


@register.filter(name='label_link')
def label_link(value):
    url = reverse('print-label')
    return f'{url}?shipments={value}'


@register.filter(name='shippop_tracking')
def shippop_tracking(value):
    return ShippopAPI().tracking_link(value)
