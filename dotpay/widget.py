# coding=utf-8
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import escape

class ModelLinkWidget(forms.HiddenInput):

    def __init__(self, admin_site, original_object):
        self.admin_site = admin_site
        self.original_object = original_object
        super(ModelLinkWidget,self).__init__()


    def render(self, name, value, attrs=None):
        if self.original_object is not None:
            link = '/admin/%s/%s/%d' % (
                self.original_object._meta.app_label,
                self.original_object._meta.module_name,
                self.original_object.pk)
            return super(ModelLinkWidget, self).render(
                name, value, attrs) + mark_safe('<a href="%s">%s</a>' % (link, escape(unicode(self.original_object))))
        else:
            return "None"

class ModelLinkAdminFields(object):
    def get_form(self, request, obj=None):
        form = super(ModelLinkAdminFields, self).get_form(request, obj)

        if hasattr(self, 'modellink'):
            for field_name in self.modellink:
                if field_name in form.base_fields:
                    form.base_fields[field_name].widget = ModelLinkWidget(self.admin_site, getattr(obj, field_name, ''))
                    form.base_fields[field_name].required = False
        return form
