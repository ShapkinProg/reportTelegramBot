from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tokenBot import token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())


class que(StatesGroup):
    Q = State()
    Q1 = State()
    Q2 = State()


def telegram_bot(token):
    b1 = KeyboardButton('Жалоба')
    b2 = KeyboardButton('Предложение')
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb_client.row(b1, b2)

    @dp.message_handler(commands='start')
    async def start_message(message: types.message):
        await bot.send_message(message.from_user.id, "Для того, чтобы отправить обратную связь, выбери тему "
                                                     "сообщения", reply_markup=kb_client)
        await que.Q.set()

    @dp.message_handler(state=que.Q)
    async def answer0_q1(message: types.Message, state: FSMContext):
        b_tema1 = KeyboardButton('Анонимно')
        kb_client_tema = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb_client_tema.row(b_tema1)
        answer = message.text
        await state.update_data(answer0=answer)
        await bot.send_message(message.from_user.id, "Теперь представься, введи своё имя, фамилию и должность, "
                                                     "если нужно:",
                               reply_markup=kb_client_tema)
        await que.next()

    @dp.message_handler(state=que.Q1)
    async def answer1_q1(message: types.Message, state: FSMContext):
        answer = message.text
        await state.update_data(answer1=answer)
        await bot.send_message(message.from_user.id, "Напиши текст сообщения:", reply_markup=ReplyKeyboardRemove())
        await que.next()

    @dp.message_handler(state=que.Q2)
    async def answer2_q1(message: types.message, state: FSMContext):
        data = await state.get_data()
        answer0 = data.get("answer0")
        answer1 = data.get("answer1")
        answer2 = message.text
        await send_mail(answer1, answer2, answer0, message)
        await state.finish()
        await bot.send_message(message.from_user.id, "Спасибо за твою обратную связь, всё передам куда нужно!😉")
        await bot.send_message(message.from_user.id, "Для того чтобы снова отправить обратную связь напиши /start ")

    executor.start_polling(dp, skip_updates=True)


async def send_mail(name_chel, bodyMes, tema, message):
    msg = MIMEMultipart()
    msg['From'] = "EmailFrom"
    msg['To'] = "EmailTo"
    msg['Subject'] = tema + "   Автор сообщения: " + str(name_chel)
    msg.attach(MIMEText(bodyMes, 'plain'))
    server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)  # ('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], "password")
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print("mail send, ura!")


if __name__ == '__main__':
    telegram_bot(token)
