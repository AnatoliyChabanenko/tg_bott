
import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        # self.loop = asyncio.get_event_loop()

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return  self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status = True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def add_phone(self,user_id, phone):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `phone1` = ? WHERE `user_id` = ?", (phone , user_id))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def get_admin(self, admin = True):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `admin1` = ?", (admin,)).fetchall()

    def add_admin(self, phone, admin = True ):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `admin1` = ? WHERE `phone1` = ?", (admin,phone))

    def get_user(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()