from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^receiver/', 'dotpay.views.receiver',name="dotpay_receiver"),
)
