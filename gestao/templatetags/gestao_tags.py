from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    request = context['request']

    dict = request.GET.copy()

    dict[field] = value

    return dict.urlencode()
