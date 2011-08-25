import django.db.models.options as options

try:
    from django.contrib.auth.models import User
    User._meta.jsonate_exclude = ('password',)
except ImportError: pass

options.DEFAULT_NAMES += ('jsonate_fields', 'jsonate_exclude')