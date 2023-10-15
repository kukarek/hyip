from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import sql
from config import MANUAL_LINK, SUPPORT

#клавиатура со списком проектов
#action - назначение клавиатуры (просмотр, удаление)
async def hyip_list_keyboard(action, user_id, message_id):
    
    projects = sql.get_hyip_projects()

    #все в столбик
    keyboard = InlineKeyboardMarkup(row_width=1)

    #построение клавиатуры с хайп проектами
    for project in projects:
        name = project[2]
        button = InlineKeyboardButton(name, callback_data=f"{action}_{user_id}_{message_id}_{name}")
        keyboard.add(button)

    keyboard.add(InlineKeyboardButton("Главное меню", callback_data=f"Главное меню_{user_id}_{message_id}"))
    return keyboard

async def hyip(link, user_id, message_id):

    keyboard = InlineKeyboardMarkup(row_width=1)

    button1 = InlineKeyboardButton("Перейти на сайт", url=link)
    button2 = InlineKeyboardButton("<- Назад", callback_data=f"Актуальные хайпы_{user_id}_{message_id}")
    keyboard.add(button1, button2)

    return keyboard

#главное меню
async def main_keyboard(user_id, message_id, status):

    #пишем сокращенно, чтобы не привысить лимит
    if status == "F":
        text = "Получать уведомления"
    else:
        text = "Запретить уведомления"

    button1 = InlineKeyboardButton("Актуальные хайпы", callback_data=f"Актуальные хайпы_{user_id}_{message_id}") 
    button2 = InlineKeyboardButton(text, callback_data=f"{text}_{user_id}_{message_id}") 
    button3 = InlineKeyboardButton("Мануал", callback_data=f"Мануал_{user_id}_{message_id}", url=MANUAL_LINK)
    button4 = InlineKeyboardButton("Поддержка", callback_data=f"Поддержка_{user_id}_{message_id}", url=SUPPORT) 

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(button1, button2, button3, button4)
    return keyboard
