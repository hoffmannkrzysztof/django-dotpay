# -*- coding: utf-8 -*-
from django.contrib import admin
from dotpay.payment.models import DotRequest,DotResponse
from dotpay.widget import ModelLinkAdminFields

class DotResponseInline(admin.StackedInline):
    model = DotResponse
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class DotResponseAdmin(ModelLinkAdminFields,admin.ModelAdmin):
    modellink = ('request',)
    list_filter = ['t_date','status','t_status','request__added']
    search_fields = ['description']
    list_display = ('__unicode__', 't_date', 't_status','amount','orginal_amount')

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
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
admin.site.register(DotResponse,DotResponseAdmin)