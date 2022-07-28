import psycopg2
from config import user, password, db_name


class SqlPython:
    def __init__(self):
        self.conn = psycopg2.connect(user=user, password=password, database=db_name)
        print("[INFO] Подключение создано", self.conn)

    # удаляем таблицу
    def dell_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                   DROP TABLE IF EXISTS clients;
               """)
        self.conn.commit()

    # создаем таблицы
    def create_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(20) NOT NULL,
            surname VARCHAR(20) NOT NULL,
            email VARCHAR(20) UNIQUE NOT NULL,
            phone_number VARCHAR(11)[] DEFAULT NULL);
            """)
            self.conn.commit()
            print("[INFO] Таблица клиенты создана")

    # Функция, позволяющая добавить нового клиента
    def add_new_client(self, f_name, s_name, e_mail, p_number=None):
        with self.conn.cursor() as cur:
            cur.execute("""
            INSERT INTO clients (first_name, surname, email, phone_number) VALUES (%s, %s, %s, %s);
            """, (f_name, s_name, e_mail, p_number))
            self.conn.commit()
            print("[INFO] Новый клиент добавлен")

    # Функия, позволвяющая получить все номера клиента
    def get_phone_numbers(self, cursor, id):
        cursor.execute("""
        SELECT phone_number FROM clients WHERE id=%s;
        """, (id,))
        return cursor.fetchone()

    # Функия, позволвяющая получить все данные клиента
    def get_client_data(self, cursor, id):
        cursor.execute("""
         SELECT * FROM clients WHERE id=%s;
         """, (id,))
        return cursor.fetchone()

    # Функция, позволяющая добавить телефон для существующего клиента
    def add_phone_number(self, id, p_number):
        with self.conn.cursor() as cur:
            numbers = self.get_phone_numbers(cur, id)[0]
            numbers += p_number
            cur.execute("""
            UPDATE clients SET phone_number=%s WHERE id=%s;
            """, (numbers, id))
            self.conn.commit()
            print("[INFO] Добавлен телефон для существующего клиента")

    # Функция, позволяющая изменить данные о клиенте
    def change_client_data(self, id, f_name, s_name, e_mail, p_number):
        with self.conn.cursor() as cur:
            cur.execute("""
            UPDATE clients SET first_name=%s, surname=%s, email=%s, phone_number=%s WHERE id=%s;
            """, (f_name, s_name, e_mail, p_number, id))
            self.conn.commit()
            print("[INFO] Данные о клиенте изменены")

    # Функция, позволяющая удалить телефон для существующего клиента
    def dell_client_phone_number(self, id, p_number):
        with self.conn.cursor() as cur:
            numbers = self.get_phone_numbers(cur, id)
            set_numbers = set()
            for i in numbers[0]:
                set_numbers.add(int(i))
            new_numbers = str(set_numbers.difference(set(p_number)))
            cur.execute("""
            UPDATE clients SET phone_number=%s WHERE id=%s;
            """, (new_numbers, id))
            self.conn.commit()
            print("[INFO] Удален телефон/телефоны для существующего клиента")

    # Функция, позволяющая удалить существующего клиента
    def dell_client(self, id):
        with self.conn.cursor() as cur:
            cur.execute("""
            DELETE FROM clients WHERE id = %s;
            """, (id,))
            self.conn.commit()
            print("[INFO] Данные о клиенте удалены")

    # Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
    def find_client(self, *data):
        if len(data) == 3:
            with self.conn.cursor() as cur:
                cur.execute("""
                SELECT * FROM clients WHERE first_name=%s and surname=%s and email=%s;
                """, (data[0], data[1], data[2],))
                print(cur.fetchall())
                print("[INFO] Данные о клиенте получены")
        elif len(data) == 1:
            with self.conn.cursor() as cur:
                cur.execute("""
                SELECT * FROM clients WHERE %s = ANY(phone_number);
                """, (str(data[0][0]), ))
                print(cur.fetchall())
                print("[INFO] Данные о клиенте получены")


if __name__ == "__main__":
    sql_req = SqlPython()
    sql_req.dell_db()
    sql_req.create_db()
    sql_req.add_new_client('Vladimir', 'Mikhaylov', 'mvi82@mail.ru', [89263696821, 89264567892])
    sql_req.add_new_client('Viktor', 'Popandopalo', 'Viktor@mail.ru', [89263696822, 89264567891])
    sql_req.add_new_client('Vlad', 'Zolotov', 'Zolotov@mail.ru')
    sql_req.add_phone_number(1, [89261234567])
    sql_req.change_client_data(1, 'Vladimir', 'Mikhaylov', 'mvi82@mail.ru', [89263696821])
    sql_req.dell_client_phone_number(1, [89264567892, 89261234567])
    sql_req.dell_client(3)
    sql_req.find_client('Viktor', 'Popandopalo', 'Viktor@mail.ru')
    sql_req.find_client([89263696821])
