# -*- coding: utf8 -*-

import json
import logging
import re
import traceback

import telepot
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from py_planet.models import TgGroup, TgUser, UserGroupModel

from .utils import parse_planetpy_rss


TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')


def _display_help():
    return render_to_string('help.md')


def _display_planetpy_feed():
    return render_to_string('feed.md', {'items': parse_planetpy_rss()})


class CommandReceiveView(View):
    def post(self, request, bot_token):
        print(dir(TelegramBot))
        try: 
            print('------------------------------------------')
            print(request.body)
            print('------------------------------------------')
            if bot_token != settings.TELEGRAM_BOT_TOKEN:
                return HttpResponseForbidden('Invalid token')

            commands = {
                '/start': _display_help,
                'help': _display_help,
                'feed': _display_planetpy_feed,
            }

            raw = request.body.decode('utf-8')
            logger.info(raw)

            try:
                payload = json.loads(raw)
            except ValueError:
                return HttpResponseBadRequest('Invalid request body')
            else:
                chat = payload['message']['chat']
                user = payload['message']['from']

                add_user_group(chat, user)
                # fuck(chat, user)
                print('chat id {}'.format(chat.get('id')))
                cmd = payload['message'].get('text')  # command
                # pattern = re.compile(u'^!выебать')
                # if pattern.match(cmd):
                #     print('MATCH------------------')

#            func = commands.get(cmd.split()[0].lower())
#            if func:
#                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
#            else:
#                pass
                #TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')
        except Exception:
            print(str(traceback.format_exc()))
            logger.error(str(traceback.format_exc()))
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)


def add_user_group(chat, user):
    print(TelegramBot.getChatMember(chat.get('id'), user['id']))
    status = TelegramBot.getChatMember(chat.get('id'), user['id']).get('status')
    print('STATUS {}'.format(status))
    if status in ['administrator', 'creator', 'member']:
        print('MEMBER!')
        try:
            db_user = TgUser.objects.get(id=user.get('id'))
        except TgUser.DoesNotExist:
            db_user = TgUser.objects.create(
                id=user.get('id'),
                first_name=user.get('first_name'),
                last_name=user.get('last_name'),
                username=user.get('username')
            )

        try:
            db_group = TgGroup.objects.get(id=chat.get('id'))
        except TgGroup.DoesNotExist:
            db_group = TgGroup.objects.create(
                id=chat.get('id'),
                title=chat.get('title')
            )

        UserGroupModel.objects.create(
            user=db_user,
            group=db_group
        )


def fuck(chat, user):
    pattern = re.compile(u'^!выебать')
                # if pattern.match(cmd):