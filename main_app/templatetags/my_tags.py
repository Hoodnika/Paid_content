from django.contrib.auth.decorators import user_passes_test
from django import template

from main_app.models import Publication

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f'/media/{path}'
    return '#'


@register.filter()
def split_filter(name):
    return name[:99]


@register.filter()
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter()
def random_publication(publication):
    return Publication.objects.filter(owner=publication.owner).order_by('?')[:1]

# @register.filter()
# def random_publication(publication_list):
#     if publication_list:
#         return publication_list.order_by('?')[:1]
#     return None
