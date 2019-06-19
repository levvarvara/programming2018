import telebot
import flask
token = '895830015:AAGkl0EPNcj52z369UCdADnm8X0i8AYpqdI'

telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который покажет графики частотности употребления тематических слов в сообществах ВК. Наберите /analise для того, чтобы получить таблицы.")


@bot.message_handler(commands=['analise'])
def echo(message):
    text = message.text
    user = message.chat.id
    bot.send_message(user, "АНАЛИТИКА ПО СООБЩЕСТВАМ КНИЖНЫХ МАГАЗИНОВ")
    bot.send_message(user, "Список анализируемых слов: автор, бестселлер, скидка, сюжет, герой, детектив, фантастика, роман, новинка, розыгрыш,классика, премия, сказка")

    bot.send_photo(user, "https://github.com/levvarvara/programming2018/blob/master/FinalProject/%D0%91%D1%83%D0%BA%D0%B2%D0%BE%D0%B5%D0%B4.png?raw=true")
    bot.send_photo(user, "https://github.com/levvarvara/programming2018/blob/master/FinalProject/%D0%9A%D0%BD%D0%B8%D0%B3%D0%B8.%20%D0%98%D0%B7%D0%B4%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D1%82%D0%B2%D0%BE%20%D0%90%D0%A1%D0%A2.png?raw=true")
    bot.send_photo(user, "https://github.com/levvarvara/programming2018/blob/master/FinalProject/%D0%9B%D0%B0%D0%B1%D0%B8%D1%80%D0%B8%D0%BD%D1%82.png?raw=true")
    bot.send_photo(user, "https://github.com/levvarvara/programming2018/blob/master/FinalProject/%D0%9B%D0%B8%D1%82%D0%A0%D0%B5%D1%81%20%D0%9A%D0%BD%D0%B8%D0%B3%D0%B8.png?raw=true")
    bot.send_photo(user, "https://github.com/levvarvara/programming2018/blob/master/FinalProject/%D1%81%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F.png?raw=true")

if __name__ == '__main__':
    bot.polling(none_stop=True)
