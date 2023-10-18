import sqlite3
from misc.config import DB

#sql запросы
def set_status(user_id, status):
   
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    # Запрос для обновления статуса по user_id
    update_status_query = f'''
    UPDATE users
    SET notify = ?
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметров new_status и user_id
    cursor.execute(update_status_query, (status, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
                
    conn.commit()
    conn.close()

def add_user(user_id):
    
    #подключение в базе данных 
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    #запрос на добавление нового юзера со статусом по умолчанию - start 

    check_user_query = f'''
    SELECT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = ?
        LIMIT 1
    );
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(check_user_query, (user_id,))
    result = cursor.fetchone()[0]

    conn.commit()
    conn.close()


    if result != 1:

        #подключение в базе данных 
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        add_user_query = f'''
        INSERT INTO users (user_id, notify)
        VALUES (?, ?);
        '''
        #Выполнение запроса с передачей параметров user_id и status
        cursor.execute(add_user_query, (user_id, "T"))
        # Сохранение изменений и закрытие подключения к базе данных
        conn.commit()
        conn.close()

def get_status(user_id):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    check_user_query = f'''
    SELECT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = ?
        LIMIT 1
    );
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(check_user_query, (user_id,))
    result = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    
    if result == 1:
       conn = sqlite3.connect(DB)
       cursor = conn.cursor()
       # Запрос для получения статуса по user_id
       get_status_query = f'''
       SELECT notify
       FROM users
       WHERE user_id = ?;
       '''
       # Выполнение запроса с передачей параметра user_id
       cursor.execute(get_status_query, (user_id,))
       status = cursor.fetchone()

       conn.commit()
       conn.close()

       return status
    
    else:
       return "0"

def get_all_users():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    get_users_query = f'''
       SELECT user_id
       FROM users;
       '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(get_users_query)
    users_id = cursor.fetchall()

    conn.commit()
    conn.close()

    return users_id

def get_users_for_notify():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = f'''
       SELECT user_id
       FROM users
       WHERE notify = ?;
       '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(query, ("T",))
    users_id = cursor.fetchall()

    conn.commit()
    conn.close()

    return users_id

def add_hyip_project(rating, name, start_date, plan, min_deposit, payment, forecast, link):
    #подключение в базе данных 
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    #запрос на добавление нового юзера со статусом по умолчанию - start 
    query = f'''
    INSERT INTO projects (rating, name, start_date, plan, min_deposit, payment, forecast, link)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    '''
    #Выполнение запроса с передачей параметров user_id и status
    cursor.execute(query, (rating, name, start_date, plan, min_deposit, payment, forecast, link))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def delete_hyip_project(name):
    
    #подключение в базе данных 
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    #запрос на удаление записи по name
    query = f'''
    DELETE FROM projects
        WHERE name = ?;
    '''
    #выполнение запроса
    cursor.execute(query, (name,))
    
    conn.commit()
    conn.close()

def get_hyip_projects():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = f'''
       SELECT *
       FROM projects;
       '''
    
    cursor.execute(query)
    hyip_projects = cursor.fetchall()

    conn.commit()
    conn.close()

    return hyip_projects

def get_hyip_project(name):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = f'''
       SELECT *
       FROM projects
       WHERE name = ?;
       '''
    
    cursor.execute(query, (name,))
    hyip_project = cursor.fetchall()

    conn.commit()
    conn.close()

    return hyip_project

#созданию соединения (используется при запуске программы, создает бд с таблицами если ее нет)
def create_connection():
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()

    # Создаем таблицу для хранения подписок пользователей, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id INTEGER PRIMARY KEY, notify TEXT)''')

    # Создаем таблицу для хранения хайп проектов, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects
                      (id INT AUTO_INCREMENT PRIMARY KEY, 
                       rating TEXT,
                       name TEXT,
                       start_date TEXT,
                       plan TEXT,
                       min_deposit TEXT,
                       payment TEXT,
                       forecast TEXT,
                       link TEXT)''')

    connection.commit()
    connection.close()
