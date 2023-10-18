from aiogram import Dispatcher, bot
from aiogram.types import CallbackQuery, Message
import keyboards
import database
from misc.config import MAIN_MESS, CHOOSE_MESS
from misc.utils import generate_hyip_info

async def on_start(message: Message):
    #добавление нового пользователя
    database.add_user(message.from_id)
    status = database.get_status(message.from_id)
    #отправка соощения с инлайн клавиатурой
    mess = await message.answer("🥳Приветствую в нашем телеграм боте!🥳\n\n" + MAIN_MESS)
    keyboard = await keyboards.main_keyboard(user_id=message.from_id, message_id=mess.message_id, status=status[0])
    await message.bot.edit_message_reply_markup(chat_id=message.from_id, message_id=mess.message_id, reply_markup=keyboard)

async def actually_hyip_button(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #кто нажал на кнопку
    message_id = int(query.data.split("_")[2]) #id сообщения с кнопкой
    
    keyboard = await keyboards.hyip_list_keyboard(action="просмотр", user_id=user_id, message_id=message_id)

    await query.bot.edit_message_text(text=CHOOSE_MESS, chat_id=user_id, message_id=message_id, reply_markup=keyboard)

async def off_notifications_button(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #кто нажал на кнопку
    message_id = int(query.data.split("_")[2]) #id сообщения с кнопкой
    
    database.set_status(user_id=user_id, status="F")

    keyboard = await keyboards.main_keyboard(user_id=user_id, message_id=message_id, status="F")

    await query.bot.edit_message_text(text=MAIN_MESS, chat_id=user_id, message_id=message_id, reply_markup=keyboard)

async def on_notifications_button(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #кто нажал на кнопку
    message_id = int(query.data.split("_")[2]) #id сообщения с кнопкой
    
    database.set_status(user_id=user_id, status="T")

    keyboard = await keyboards.main_keyboard(user_id=user_id, message_id=message_id, status="T")
    await query.bot.edit_message_text(text=MAIN_MESS + "\n\nБот будет уведомлять о вас о новых проектах!", chat_id=user_id, message_id=message_id, reply_markup=keyboard)

async def main_button(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #кто нажал на кнопку
    message_id = int(query.data.split("_")[2]) #id сообщения с кнопкой
    
    status = database.get_status(user_id=user_id)[0]

    keyboard = await keyboards.main_keyboard(user_id=user_id, message_id=message_id, status=status)

    await query.bot.edit_message_text(text=MAIN_MESS, chat_id=user_id, message_id=message_id, reply_markup=keyboard)

async def view_hyip_button(query: CallbackQuery):
    user_id = int(query.data.split("_")[1]) #кто нажал на кнопку
    message_id = int(query.data.split("_")[2]) #id сообщения с кнопкой
    hyip_project_name = query.data.split("_")[3] #имя проекта, на который нажали

    project = database.get_hyip_project(name=hyip_project_name)

    info = generate_hyip_info(project)

    keyboard = await keyboards.hyip(project[0][8], user_id=user_id, message_id=message_id)

    await query.bot.edit_message_text(text=info, chat_id=user_id, message_id=message_id, reply_markup=keyboard)
