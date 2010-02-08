import Image
import os
import sha
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import iri_to_uri, force_unicode

from fontreplacement.extras import generate_image

register = template.Library()

def get_replacementfont_setting(setting, override=None):
    """
    Get a given setting from the settings
    if override is None the setting is required
    """
    if override is not None:
        return override
    setting_key = 'REPLACEMENTFONT_%s' % setting.upper()
    if hasattr(settings, setting_key):
        return getattr(settings, setting_key)
    else:
        raise ImproperlyConfigured(u'%s is required in the settings file'
                                   % setting_key)

def get_replacementfont_kwargs(kwargs):
    """
    Changes the given string into kwargs
    """
    attrs = dict()
    if kwargs:
        for kwarg in kwargs.split(','):
            key_value = kwarg.replace(' ','').split('=')
            attrs[key_value[0]] = key_value[1]
    return attrs

@register.filter(name='fontreplacement')
@stringfilter
def fontreplacement(text, kwargs=None):
    """
    Changes a given unicode string into a
    accessible image text replacement
    TODO: Validate file exist, define max-width
    """
    kwargs = get_replacementfont_kwargs(kwargs)
    root = get_replacementfont_setting('root')
    url = get_replacementfont_setting('url')
    font_face = get_replacementfont_setting('face',
                                            kwargs.get('font'))
    size = int(get_replacementfont_setting('size',
                                           kwargs.get('size')))
    colour = get_replacementfont_setting('colour',
                                         kwargs.get('colour'))
    image_key = '%s%s%s%s' % (force_unicode(text), font_face,
                              size, colour)
    image_name = '%s.png' % sha.new(image_key).hexdigest()
    font_file = os.path.join(root, font_face)
    image_destination = os.path.join(root, image_name)
    if not os.path.isfile(image_destination):
        image = generate_image(text, font_file,
                               size, colour, image_destination)
    else:
        # we open it, since we need the
        # width and height
        image = Image.open(image_destination)
    image_url = iri_to_uri('/'.join( (url, image_name) ))
    css ="background:url(%s) transparent top left no-repeat;width:%dpx; \
          height:%dpx;" % (image_url, image.size[0], image.size[1])
    html = '<span style="text-indent:-5000px;display:block;overflow:hidden; \
           %s">%s</span>' % (css, text)
    # TODO mark_safe
    return html
