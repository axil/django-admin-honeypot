from .forms import HoneypotLoginForm
from .models import LoginAttempt
from .signals import honeypot
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _

def admin_honeypot(request, extra_context=None):
    if not request.path.endswith('/'):
        return redirect(request.path + '/', permanent=True)
    path = request.get_full_path()

    context = {
        'app_path': path,
        'form': HoneypotLoginForm(request, request.POST or None),
        REDIRECT_FIELD_NAME: path,
        'site': Site.objects.get_current(),
        'title': _('Log in'),
        'fake_admin': True,
        }
    context['form'].is_valid()
    context.update(extra_context or {})
    if len(path)>255:
        path = path[:230] +  '...(%d chars)' % len(path)
    if request.method == 'POST':
        failed = LoginAttempt.objects.create(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            session_key=request.session.session_key,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT'),
            path=path,
            )
        honeypot.send(sender=LoginAttempt, instance=failed, request=request)
    return render_to_response('admin/login.html', context, context_instance=RequestContext(request))
