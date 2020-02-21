import telebot, opts, work_with_json


class notification:
    bot = telebot.TeleBot(opts.TOKEN)
    def __init__(self):
        pass
        
    @bot.message_handler(commands=['start'])
    def start_message(self,message):
        mess = '''Здравстуйте, мой повелитель!
        Я создан, чтобы напоминать вам об вашем расписании в университете.
        Сюда будут приходить сообщение с расписанием на какой-то день,
        а также напоминание о занятиях.'''
        self.bot.send_message(message.chat.id, mess)


    #FUNCRTION TO SEND SCHEDULE TO USER AS ANSVER FOR HIS REQUEST IN VOICE ASSISTANT
    def send_schedule(self, schedule):
        content = work_with_json.read_from_file()
        self.bot.send_message(content['chat_id'], schedule)

