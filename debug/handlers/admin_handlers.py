from aiogram import Dispatcher
from aiogram.types import Message
from misc.utils import sendall
import database
from filter import isAdmin
from misc.config import HELP, ADMINS


async def help(message: Message):

    if isAdmin(message.from_id):
        message.answer(HELP) 

async def echo(message: Message):

    if not isAdmin(message.from_id):
        return
    
    #добавление администратора
    #если команда указана в начале
    if "add" == message.text.split(" ", 1)[0]:
        admin_id = int(message.text.split(" ")[1])
        ADMINS.append(admin_id)
        await message.answer(f"Добавлен администратор с id: {admin_id}")
    
    elif "user amount" == message.text:
        
        #принимаем массив кортежей из бд
        users = database.get_all_users()
        notify_users = database.get_users_for_notify()

        await message.answer(f"Количество пользователей: {len(users)}\n"+
                                f"Включена рассылка: {len(notify_users)}")
    
    #если команда указана в начале
    elif "sendall" in message.text.split("\n", 1)[0]:
        
        #берем сообщение после команды sendall
        mess = message.text.split("\n", 1)[1]
        
        await sendall(mess)

    elif "add_hyip" == message.text.split("\n", 1)[0]:

        try:
            mess = message.text.split("\n")

            database.add_hyip_project(rating=mess[1],
                                name=mess[2],
                                start_date=mess[3],
                                plan=mess[4],
                                min_deposit=mess[5],
                                payment=mess[6],
                                forecast=mess[7],
                                link=mess[8])
        except Exception as e:
            await message.answer(e)
    
    elif "delete_hyip" == message.text.split("\n", 1)[0]:

        try:
            mess = message.text.split("\n")

            database.delete_hyip_project(name=mess[1])
        except Exception as e:
            await message.answer(e)




    