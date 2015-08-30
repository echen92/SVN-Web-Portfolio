from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter()
@stringfilter
def replace_bad_words(value):
    value = value.lower()
    swear_list = ['fuck', 'shit', 'bitch', 'whore', 'cunt', 'nigger']
    words_seen = [w for w in swear_list if value.find(w) is not -1]
    if words_seen:
        for word in words_seen:
            value = value.replace(word, "%s" % ('*'*(len(word))))
    return value
