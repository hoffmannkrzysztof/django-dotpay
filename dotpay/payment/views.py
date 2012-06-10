import logging
import urlparse
from django.views.decorators.csrf import csrf_exempt
from dotpay.payment.models import DotResponse
from django.http import HttpResponse
from dotpay.payment.util import DOTPAY_SERVERS

@csrf_exempt
def receiver(request):
    if request.POST:
        if request.META['REMOTE_ADDR'] in DOTPAY_SERVERS:
            vars = {}
            try:
                post = urlparse.parse_qs(request._raw_post_data)
            except AttributeError:
                post = request.POST
            for field in DotResponse._meta.fields:
                if field.name != 'request':
                    var = post.get(field.name, None)
                    if var:
                        if type(var) == list:
                            var = var[0].decode("iso8859-2")
                        elif type(var) == str:
                            var = var.decode("iso8859-2")
                    vars[field.name] = var
            try:
                dotresponse = DotResponse.objects.get_or_create(control=vars.pop('control'),
                                                                t_id=vars.pop('t_id'),
                                                                defaults=vars)
            except Exception, e:
                return HttpResponse("ERR", status=500)
            else:
                return HttpResponse("OK", status=200)
        else:
            return HttpResponse("ERR", status=403)
    else:
        return HttpResponse("405 Method Not Allowed", status=405)
