from django.contrib import admin
from .models import LoginAttempt

class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_ip_address', 'get_session_key', 'timestamp', 'get_path')
    list_filter = ('timestamp',)
    readonly_fields = ('username', 'password', 'ip_address', 'session_key', 'user_agent')
    search_fields = ('username', 'password', 'ip_address', 'user_agent', 'path')

    def get_session_key(self, instance):
        return '<a href="?session_key=%(key)s">%(key)s</a>' % {'key': instance.session_key}
    get_session_key.short_description = 'Session'
    get_session_key.allow_tags = True

    def get_ip_address(self, instance):
        return '<a href="?ip_address=%(ip)s">%(ip)s</a>' % {'ip': instance.ip_address}
    get_ip_address.short_description = 'IP Address'
    get_ip_address.allow_tags = True
    
    def get_path(self, instance):
        return '<a href="?path=%(path)s">%(path)s</a>' % {'path': instance.path}
    get_path.short_description = 'URL'
    get_path.allow_tags = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(LoginAttempt, LoginAttemptAdmin)
