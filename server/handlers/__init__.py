from aiogram import Dispatcher
from .admin_handlers import *
from .user_handlers import *



def register_all_handlers(dp: Dispatcher) -> None:
    #user
    dp.register_message_handler(on_start, commands=['start'])
    dp.register_callback_query_handler(actually_hyip_button, lambda query: query.data.startswith("Актуальные хайпы"))
    dp.register_callback_query_handler(off_notifications_button, lambda query: query.data.startswith("Запретить уведомления"))
    dp.register_callback_query_handler(on_notifications_button, lambda query: query.data.startswith("Получать уведомления"))
    dp.register_callback_query_handler(main_button, lambda query: query.data.startswith("Главное меню"))
    dp.register_callback_query_handler(view_hyip_button, lambda query: query.data.startswith("просмотр"))
    #admin
    dp.register_message_handler(echo)
    dp.register_message_handler(help, commands=['help'])

