from .signals import honeypot
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import mail_admins
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

def notify_admins(instance, request, **kwargs):
    app_name = __name__.split('.')[-2]
    context = {
        'request': request,
        'instance': instance,
        'site': get_current_site(request),
        'url': reverse('admin:%s_loginattempt_change' % app_name, args=[instance.pk]),
        }
    subject = render_to_string('admin_honeypot/email_subject.txt', context).strip()
    message = render_to_string('admin_honeypot/email_message.txt', context).strip()
    mail_admins(subject=subject, message=message)

if getattr(settings, 'ADMIN_HONEYPOT_EMAIL_ADMINS', True):
    honeypot.connect(notify_admins)
