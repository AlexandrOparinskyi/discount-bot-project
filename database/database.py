import sqlite3
from typing import NoReturn


class ConnectDB:

    def __init__(self, db_name) -> NoReturn:
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()

    def exists_user(self, user_id) -> bool:
        """Проверка наличия пользователя в БД"""
        result = self.cursor.execute(
            "SELECT * FROM 'users' WHERE user_id = ?", (user_id,)
        )
        return bool(result.fetchone())

    def add_user(self, user_id) -> NoReturn:
        """Добавление пользователя в БД"""
        self.cursor.execute(
            "INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,)
        )
        return self.connect.commit()

    def exists_item(self, article) -> bool:
        """Проверка наличия товара в БД"""
        result = self.cursor.execute(
            "SELECT 'id' FROM 'items' WHERE article = ?", (article,)
        )
        return bool(result.fetchall())

    def add_item(self, article, title, url, img, api_url) -> NoReturn:
        """Добавление товара в БД"""
        self.cursor.execute(
            "INSERT INTO 'items' ('article', 'title', 'url', 'image', "
            "'api_url') VALUES (?, ?, ?, ?, ?)",
            (article, title, url, img, api_url)
        )
        return self.connect.commit()

    def close(self) -> NoReturn:
        """Закрытие БД"""
        self.connect.close()
