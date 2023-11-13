import g4f
import telebot
from config import TOKEN, ADMIN_ID

# НАСТРОЙКИ БОТА
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# НАСТРОЙКИ CHAT_GPT
g4f.logging = True
g4f.check_version = False


def ask_gpt(promt) -> str:
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": promt}],
        stream=True,
    )

    ans_message = ''
    for message in response:
        ans_message += message

    return ans_message


@bot.message_handler()
def ask_bot(message):
    if ADMIN_ID is None:
        question = message.text
        answer = ask_gpt(question)
        bot.reply_to(message, answer)
    else:
        if message.from_user.id == ADMIN_ID:
            question = message.text
            answer = ask_gpt(question)
            bot.reply_to(message, answer)

        else:
            bot.reply_to(message, 'Доступ запрещён!')


bot.infinity_polling()