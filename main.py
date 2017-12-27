# -*- coding: utf-8 -*-
import telebot
import configparser
import sys
import logging
import flask
import sequencer
import sqlprovider
import Accaunting
from telebot import types
# Храним конфиги бота в файле ini
config = configparser.ConfigParser()
config.read('config.ini')

# Токен бота и путь до базыданных со схемой логики
API_TOKEN = config['DEFAULT']['Token']
STATIC_SCHEMA = config['DEFAULT']['Schema']

# Конфиги веб хуков бота
WEBHOOK_HOST = config['DEFAULT']['Host']
WEBHOOK_PORT = config['DEFAULT']['Port']
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = config['DEFAULT']['CERT']  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = config['DEFAULT']['PRIV']  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

WELCOME_PAGE = 'welcome_page'

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# Иницализируем бот и веб сервер для хуков
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)


# Игнорируем запросы страници index
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Получаем хуки и обновляем бота
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


# Инициализациия процесса логики
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    uid = message.chat.id
    user = message.chat
    # print(uid)
    client = get_client(uid, user)
    client.goto(WELCOME_PAGE)
    send_page(uid, client.cur_page)
    # print('end_send')


def get_client(uid, user):
    if Accaunting.is_registered(uid):
        client = Accaunting.get_user(uid)
    else:
        client = Accaunting.User(uid, user.username,
                                 user.first_name, user.last_name)
        # client.goto(WELCOME_PAGE)
        # logger.makeRecord()
    return client


# Обробатывем любые текстовые пакеты
@bot.message_handler(func=lambda message: True, content_types=['text'])
def proc_req(message):
    # print('start_step')
    uid = message.chat.id
    user = message.chat
    client = get_client(uid, user)
    # print('DANGER')
    ac = schema_provider.get_action_by_text(message.text)
    # print('poof')
    user_action(client, ac)
    send_page(uid, client.cur_page)
    # print('end_step')


def user_action(user, ac):
    action_parser = sequencer.Sequence(action_handler=lambda ct, a, ar: (ct, a, ar))
    # print(ac)
    context, action, arguments = action_parser.parse(ac)
    # print(context)
    # print(action)
    # print(arguments)
    if action == 'goto':
        user.goto(arguments[0])
    if action == 'back':
        user.back()


def send_page(chat_id, page):
    # print(page)
    try_page = sqlprovider.Page(schema_provider, page)
    content_parser = sequencer.Sequence(lambda tn, cn, co: (tn, cn, co))
    type_s, cname, column = content_parser.parse(try_page.content)
    content = schema_provider.get_static_text(cname)
    # print(content)
    # print(type_s)
    if type_s == 'static_strings':
        # pass
        # print(type_s)
        bot.send_message(chat_id, content, reply_markup=get_markup(try_page.menu))


def get_markup(menu):
    markup = types.ReplyKeyboardMarkup()
    for it in menu.inputs:
        markup.add(types.KeyboardButton(it.text))
    return markup


# 4100 1585 0030 163?
def main(argv):
    global schema_provider
    schema_provider = sqlprovider.Provider(STATIC_SCHEMA)

    # Прикрепляем новый хук
    # bot.remove_webhook()
    # bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
    #                 certificate=open(WEBHOOK_SSL_CERT))
    bot.polling(none_stop=True)
    # И зарускаем веб сервер
    # app.run(host=WEBHOOK_LISTEN,
    #         port=WEBHOOK_PORT,
    #         ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
    #         debug=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

