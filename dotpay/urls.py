from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^receiver/', 'dotpay.payment.views.receiver',name="dotpay_receiver"),
)
