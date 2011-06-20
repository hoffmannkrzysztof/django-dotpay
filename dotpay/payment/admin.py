from django.contrib import admin
from dotpay.payment.models import DotRequest,DotResponse

class DotResponseInline(admin.StackedInline):
    model = DotResponse
    extra = 0
    can_delete = False
    
class DotRequestAdmin(admin.ModelAdmin):
    inlines = [DotResponseInline,]
    search_fields = ['opis','email']
    list_display = ('opis', 'email', 'added')
    list_filter = ['added',]
    
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(DotRequest, DotRequestAdmin)