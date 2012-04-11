from django.contrib.auth.models import User
from django.db import models
from dotpay.payment.models import DotRequest

class Order(models.Model):
    user = models.ForeignKey(User)
    request = models.OneToOneField(DotRequest)

