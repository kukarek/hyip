import database




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

#рассылка всем пользователям
async def sendall(bot, message):
    #принимаем массив кортежей из бд
    users = database.get_users_for_notify()
    
    for user in users:
        try:
            await bot.send_message(user[0], message)
        except Exception as e:
            print(f"Ошибка рассылки юзеру: {e}")
