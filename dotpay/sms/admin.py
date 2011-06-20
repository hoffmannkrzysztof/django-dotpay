from django.contrib import admin
from dotpay.sms.models import DotSms

    
class DotSmsAdmin(admin.ModelAdmin):
    search_fields = ['code',]
    list_display = ('code', 'value', 'added')
    list_filter = ['added',]
    
    def has_add_permission(self, request, obj=None):
        return False
    

admin.site.register(DotSms, DotSmsAdmin)