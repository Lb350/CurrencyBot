import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '❗️Чтобы начать работу введите команду боту в следующем формате:\n\
1️⃣<валюта, которую необходимо перевести>\n\
2️⃣<в какую валюту перевести>\n\
3️⃣<количество переводимой валюты>\n\
❗️Пример: доллар рубль 50\n\
➡️Чтобы увидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = '⬇️Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,'💸' + key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('‼️Ошибка в параметрах запроса.\nПравильный формат указан в /help')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'‼️Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'‼️Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
