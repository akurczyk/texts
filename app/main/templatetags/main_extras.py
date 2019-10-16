from django import template
from django.db.models import Sum
from django.db.models.functions import Coalesce

from ..models import Text

register = template.Library()


@register.simple_tag
def get_3_random_texts():
    return Text.objects \
        .filter(processed=True) \
        .filter(published=True) \
        .order_by('?')[:3]


@register.simple_tag
def get_3_best_texts():
    return Text.objects \
        .filter(processed=True) \
        .filter(published=True) \
        .annotate(votes_count=Coalesce(Sum('vote__vote'), 0))\
        .order_by('-votes_count')[:3]


@register.simple_tag
def get_3_newest_texts():
    return Text.objects \
        .filter(processed=True) \
        .filter(published=True) \
        .order_by('-id')[:3]
