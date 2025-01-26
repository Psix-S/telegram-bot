import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import random

# Замените YOUR_TOKEN на ваш токен бота
TOKEN = "6084652350:AAGAwkKCi47d3awsZXWd3owxLHEgxDHhbL0"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    if user and user.first_name:
        name = user.first_name
    elif user and user.username:
        name = user.username
    else:
        name = "друг"
    context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Приветствую, {name}! Добро пожаловать в наш клановый чат! Напиши 'игра' для начала игры.")
    context.user_data['game_state'] = None

def handle_member_removed(update: Update, context: CallbackContext):
    print(f"Chat member update: {update.chat_member}")
    if update.chat_member.old_chat_member.status in ["member", "administrator"]:
        print(f"old chat member status: {update.chat_member.old_chat_member.status}")
        user = update.chat_member.old_chat_member.user

        if user and (user.first_name or user.username):
            if user.first_name:
              name = user.first_name
            elif user.username:
              name = user.username
            else:
              name = "друг"
            context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Прощай, {name} мерзость! Надеемся, что ты никогда не будешь вонять в нашем клане!")

def handle_new_chat_members(update: Update, context: CallbackContext):
   for user in update.message.new_chat_members:
       if not user.is_bot:
            if user.first_name:
               name = user.first_name
            elif user.username:
               name = user.username
            else:
              name = "друг"
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Добро пожаловать в наш самый ахуенный клан, {name}!")

def handle_message(update: Update, context: CallbackContext):
        print("Вызвана handle message")
        message_text = update.message.text.lower()
        print(message_text)
        phrases = {
            ("зик привет", "привет зик", "здорова зик", "зик здорова"): [
                "Салют!",
                "Здарова!",
                "Приветствую!",
                "И тебе не хворать!",
                "Чо как!"
            ],
            ("зик пока", "пока зик", "прощай зик", "зик прощай"): [
                "Ауфвидерзеен!",
                "Счастливо!",
                "Пока!",
                "До скорого!",
                "Свидимся!"
            ],
            ("зик как дела", "как дела зик", "как ты зик", "зик как ты"): [
                "Все заебись ты как не помер еще?",
                "Да ниче, норм, а у тебя чо как?",
                "Да как обычно, чо каво!",
                "Не жалуюсь, а сам как?",
                "Все путем, как сам поживаешь?"
            ],
            ("кто я", "кто я такой"): [
              "Ты - легенда!",
              "Ты - загадочная личность!",
              "Ты - мой хороший раб!",
              "Ты - лучший человек на свете!",
              "Ты - мой пидручух!",
              "Ты - сморщенная холка",
              "Ты - милашка"
            ]
        }

        if context.user_data.get('game_state') == None:
              if message_text == "игра":
                 context.user_data['game_state'] = 'start'
                 context.bot.send_message(chat_id=update.effective_chat.id, text="Ты в рси бомбе. Перед тобой два варианта: крысить и рашить. Как сыгрешь? (напиши 'крысить' или 'рашить')")
                 return
        if context.user_data.get('game_state') == 'start':
              if message_text == 'рашить':
                  context.user_data['game_state'] = 'left_path'
                  context.bot.send_message(chat_id=update.effective_chat.id, text="Ты убил 4 из 5 противников и остался 1 что будешь делать искать последнего или сидеть? (напиши 'искать' или 'сидеть')")
                  return
              elif message_text == 'крысить':
                 context.user_data['game_state'] = 'right_path'
                 context.bot.send_message(chat_id=update.effective_chat.id, text="Ты встретил араба! Что будешь делать? (напиши 'сражаться' или 'убежать')")
                 return
        elif context.user_data.get('game_state') == 'left_path':
           if message_text == 'искать':
              context.user_data['game_state'] = 'left_path'
              context.bot.send_message(chat_id=update.effective_chat.id, text="Ты нашел эту крысу и нагнул ее на член! (Игра окончена ты сделал эйс)")
              context.user_data['game_state'] = None
              return
           elif message_text == "сидеть":
                context.user_data['game_state'] = None
                context.bot.send_message(chat_id=update.effective_chat.id, text="Тебя взяли на расправу и ты сдох как лох! (Игра окончена нубяра)")
                return
        elif context.user_data.get('game_state') == 'right_path':
            if message_text == 'сражаться':
               context.user_data['game_state'] = None
               context.bot.send_message(chat_id=update.effective_chat.id, text="Ты сразился с арабом и погиб, это же араб долбаеб! (Игра окончена сдох как лох)")
               return
            elif message_text == "убежать":
                context.user_data['game_state'] = None
                context.bot.send_message(chat_id=update.effective_chat.id, text="Ты убежал от араба и вы загасили его всей толпой! (Игра окончена топор гасит даже араба)")
                return
        for phrase_set, responses in phrases.items():
          if message_text in phrase_set:
            context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(responses))
            return


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(ChatMemberHandler(handle_member_removed, ChatMemberHandler.CHAT_MEMBER))
    dp.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_chat_members))
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    updater.start_webhook(listen="0.0.0.0", port=80, url_path="/")
    updater.bot.set_webhook("https://telegram-bot-sigma-amber.vercel.app/" + "/") # <---- ВОТ ТУТ ВАМ НУЖНО ЗАМЕНИТЬ
    updater.idle()


if __name__ == '__main__':
    main()