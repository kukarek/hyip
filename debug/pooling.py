import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.types import CallbackQuery
import sql
import keyboards
from config import API_TOKEN, ADMINS, MAIN_MESS, CHOOSE_MESS, HELP

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def admin(id):
    for admin in ADMINS:
        if admin == id:
            return True
    return False

    
@dp.callback_query_handler(lambda query: query.data.startswith("Актуальные хайпы"))
async def on_button1_click(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #кто нажал на кнопку
    message_id = int(query.data.split("_")[2]) #id сообщения с кнопкой
    
    keyboard = await keyboards.hyip_list_keyboard(action="просмотр", user_id=user_id, message_id=message_id)

    await bot.edit_message_text(text=CHOOSE_MESS, chat_id=user_id, message_id=message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data.startswith("Запретить уведомления"))
async def on_button1_click(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #кто нажал на кнопку
    message_id = int(query.data.split("_")[2]) #id сообщения с кнопкой
    
    sql.set_status(user_id=user_id, status="F")

    keyboard = await keyboards.main_keyboard(user_id=user_id, message_id=message_id, status="F")

    await bot.edit_message_text(text=MAIN_MESS, chat_id=user_id, message_id=message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data.startswith("Получать уведомления"))
async def on_button1_click(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #кто нажал на кнопку
    message_id = int(query.data.split("_")[2]) #id сообщения с кнопкой
    
    sql.set_status(user_id=user_id, status="T")

    keyboard = await keyboards.main_keyboard(user_id=user_id, message_id=message_id, status="T")
    await bot.edit_message_text(text=MAIN_MESS + "\n\nБот будет уведомлять о вас о новых проектах!", chat_id=user_id, message_id=message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data.startswith("Главное меню"))
async def on_button1_click(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #кто нажал на кнопку
    message_id = int(query.data.split("_")[2]) #id сообщения с кнопкой
    
    status = sql.get_status(user_id=user_id)[0]

    keyboard = await keyboards.main_keyboard(user_id=user_id, message_id=message_id, status=status)

    await bot.edit_message_text(text=MAIN_MESS, chat_id=user_id, message_id=message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data.startswith("просмотр"))
async def on_button1_click(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #кто нажал на кнопку
    message_id = int(query.data.split("_")[2]) #id сообщения с кнопкой
    hyip_project_name = query.data.split("_")[3] #имя проекта, на который нажали

    project = sql.get_hyip_project(name=hyip_project_name)

    info = generate_hyip_info(project)

    keyboard = await keyboards.hyip(project[0][8], user_id=user_id, message_id=message_id)

    await bot.edit_message_text(text=info, chat_id=user_id, message_id=message_id, reply_markup=keyboard)

#преобразование данных из бд в читабельный текст
def generate_hyip_info(hyip):

    rating = ""
    i = 0
    while i < int(hyip[0][1]):
        rating += "⭐️"
        i += 1

    mess = (f"Рейтинг:\n{rating}\n\n"+
            f"♨️{hyip[0][2]}♨️\n\n"+
            f"🏁Дата запуска: {hyip[0][3]}\n\n"+
            f"📊План: {hyip[0][4]}\n\n"+
            f"💵Минимальный депозит: {hyip[0][5]}\n\n"+
            f"💸Платежные системы: {hyip[0][6]}\n\n"+
            f"📈Прогноз наших админов: {hyip[0][7]}\n\n")
    
    return mess

async def sendall(message):
    #принимаем массив кортежей из бд
    users = sql.get_users_for_notify()
    
    for user in users:
        try:
            await bot.send_message(user[0], message)
        except Exception as e:
            print(f"Ошибка рассылки юзеру: {e}")

@dp.message_handler(commands=['start'])
async def on_start(message: Message):
    #добавление нового пользователя
    sql.add_user(message.from_id)
    status = sql.get_status(message.from_id)
    #отправка соощения с инлайн клавиатурой
    mess = await message.answer("🥳Приветствую в нашем телеграм боте!🥳\n\n" + MAIN_MESS)
    keyboard = await keyboards.main_keyboard(user_id=message.from_id, message_id=mess.message_id, status=status[0])
    await bot.edit_message_reply_markup(chat_id=message.from_id, message_id=mess.message_id, reply_markup=keyboard)

@dp.message_handler(commands=['help'])
async def on_start(message: Message):

    if admin(message.from_id):

        await message.answer(HELP)
    

#возвращаем True, если было действие с админ панелью    
async def admin_panel(message):

    if admin(message.from_id):
        #добавление администратора
        #если команда указана в начале
        if "add" == message.text.split(" ", 1)[0]:
            admin_id = int(message.text.split(" ")[1])
            ADMINS.append(admin_id)
            await message.answer(f"Добавлен администратор с id: {admin_id}")
            return True
        
        elif message.text == "user amount":
            
            #принимаем массив кортежей из бд
            users = sql.get_all_users()
            notify_users = sql.get_users_for_notify()

            await message.answer(f"Количество пользователей: {len(users)}\n"+
                                 f"Включена рассылка: {len(notify_users)}")
            return True
        
        #если команда указана в начале
        elif "sendall" in message.text.split("\n", 1)[0]:
            
            #берем сообщение после команды sendall
            mess = message.text.split("\n", 1)[1]
            
            await sendall(mess)

            return True

        elif "add_hyip" == message.text.split("\n", 1)[0]:

            try:
                mess = message.text.split("\n")

                sql.add_hyip_project(rating=mess[1],
                                    name=mess[2],
                                    start_date=mess[3],
                                    plan=mess[4],
                                    min_deposit=mess[5],
                                    payment=mess[6],
                                    forecast=mess[7],
                                    link=mess[8])
            except Exception as e:
                await message.answer(e)
            return True
        
        elif "delete_hyip" == message.text.split("\n", 1)[0]:

            try:
                mess = message.text.split("\n")

                sql.delete_hyip_project(name=mess[1])
            except Exception as e:
                await message.answer(e)
            return True
            
        
    return False

@dp.message_handler()
async def echo(message: Message):
    
    try:
        if await admin_panel(message):
            return
    except Exception as e:
        await message.answer(e)
        return
    
    await message.answer("Выберите действие на клавиатуре!")

def main():
    # Запуск бота
    sql.create_connection()
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()