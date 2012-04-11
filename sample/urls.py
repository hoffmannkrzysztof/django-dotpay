from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dotpay/', include('dotpay.urls')),
    (r'form/','sample.order.views.form'),
    (r'form-sms/','sample.sms.views.form'),
)
