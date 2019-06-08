import hashlib
from urllib.parse import urlencode

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def gravatar(user):
    email = user.lower().encode('utf-8')
    default = 'mm'
    size = 80

    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urlencode({'d':default, 's':str(size)})
    url = gravatar_url
    return url
