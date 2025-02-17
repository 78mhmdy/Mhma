

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = '7511938455:AAE99I9njQWTe7NIe9vqEIgiWB9f_Z8KnR0'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('مرحبًا! استخدم /set_source لتحديد القناة المصدر و /set_target لتحديد القناة الهدف.')

def set_source(update: Update, context: CallbackContext):
    global source_chat_id
    source_chat_id = update.message.text
    update.message.reply_text(f'تم تعيين القناة المصدر: {source_chat_id}')

def set_target(update: Update, context: CallbackContext):
    global target_chat_id
    target_chat_id = update.message.text
    update.message.reply_text(f'تم تعيين القناة الهدف: {target_chat_id}')

def forward_message(update: Update, context: CallbackContext):
    global source_chat_id, target_chat_id
    if source_chat_id and target_chat_id:
        if str(update.message.chat_id) == source_chat_id:
            update.message.forward(chat_id=target_chat_id)
    else:
        update.message.reply_text('يرجى تعيين القناة المصدر والهدف أولاً.')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set_source", set_source))
    dp.add_handler(CommandHandler("set_target", set_target))
    dp.add_handler(MessageHandler(filters.text & ~filters.command, forward_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()