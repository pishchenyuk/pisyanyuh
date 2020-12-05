import requests
import telebot


def messages(token):
    url = 'https://api.vk.com/method/messages.getDialogs?access_token=' + token + '&v=5.60&unread=1'
    s = requests.Session()
    json = s.get(url).json()['response']
    dialogs = json['count']
    json = json['items']
    array = []
    for i in range(dialogs):
        title = json[i]['message']['title']
        # print(json[i]['message'])
        body = json[i]['message']['body']
        if body != '':
            array.append(title + ':\t\t\t' + body)
    return array


bot = telebot.TeleBot(token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Узнать баланс QIWI', 'VK', 'Кит')

VKKeyboard = telebot.types.ReplyKeyboardMarkup(True, True)
VKKeyboard.row('Переписки', 'Изменить статус')

cancel = telebot.types.ReplyKeyboardMarkup(True, True)
cancel.row('Отмена')

# Баланс QIWI Кошелька
def balance(login, api_access_token):
    s = requests.Session()
    s.headers['Accept'] = 'application/json'
    s.headers['authorization'] = 'Bearer ' + api_access_token
    b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + login + '/accounts')
    print()
    balances = b.json()['accounts']
    rubAlias = [x for x in balances if x['alias'] == 'qw_wallet_rub']
    rubBalance = rubAlias[0]['balance']['amount']
    return rubBalance



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я микро-бот @pisyanyuh, дабы упростить некоторые его идеи...',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def dialog(message):
    if message.chat.id != 984232674 and message.chat.id != 705623785:
        bot.send_message(message.chat.id, 'Слыш, тебе сюда нельзя')
        print(message.chat.id)
    elif message.text == 'Узнать баланс QIWI':
        bot.send_message(message.chat.id, str(balance(mylogin, api_access_token))[:3] + ' рублей', reply_markup=keyboard1)
    elif message.text == 'VK':
        bot.send_message(message.chat.id, 'Хорошо, выбирай:', reply_markup=VKKeyboard)
    elif message.text == 'Кит':
        a = requests.Session().get('https://aws.random.cat/meow').json()
        bot.send_photo(message.chat.id, a['file'], reply_markup=keyboard1)
    elif message.text == 'Переписки':
        k = messages(vk_api)
        for i in k:
            bot.send_message(message.chat.id, i, reply_markup=keyboard1)
    elif message.text == 'Изменить статус':
        if message.chat.id != 984232674:
            bot.send_message(message.chat.id, 'Слыш, вышел вон!1')
        else:
            msg = bot.send_message(message.chat.id, 'Введите желаемый статус:', reply_markup=cancel)
            bot.register_next_step_handler(msg, changeStatus)
def changeStatus(message):
    status = message.text.replace(' ', '%20')
    url = 'https://api.vk.com/method/status.set?access_token=' + vk_api + '&v=5.60&text=' + status
    s = requests.Session()
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Отменил!', reply_markup=keyboard1)
        return
    j = s.get(url).json()
    if j['response'] == 1:
        bot.send_message(message.chat.id, 'Готово, изменил статус!', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Всё хуйня', reply_markup=keyboard1)
bot.polling(none_stop=True)