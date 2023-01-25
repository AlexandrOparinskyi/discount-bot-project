import sqlite3
from typing import NoReturn, Union


class ConnectDB:

    def __init__(self, db_name) -> NoReturn:
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()

    def exists_user(self, user_id: int) -> bool:
        """Проверка наличия пользователя в БД"""
        result = self.cursor.execute(
            "SELECT * FROM 'users' WHERE user_id = ?", (user_id,)
        )
        return bool(result.fetchone())

    def add_user(self, user_id: int) -> None:
        """Добавление пользователя в БД"""
        self.cursor.execute(
            "INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,)
        )
        return self.connect.commit()

    def exists_item(self, article: str) -> bool:
        """Проверка наличия товара в БД"""
        result = self.cursor.execute(
            "SELECT 'id' FROM 'items' WHERE article = ?", (article,)
        )
        return bool(result.fetchall())

    def add_item(self, article: str, title: str, url: str, img: str,
                 api_url: str, price: int, sale_price: int = None) -> None:
        """Добавление товара в БД"""
        self.cursor.execute(
            "INSERT INTO 'items' ('article', 'title', 'url', 'image', "
            "'api_url', 'price', 'sale_price') VALUES (?, ?, ?, ?, ?, ?, ?)",
            (article, title, url, img, api_url, price, sale_price)
        )
        return self.connect.commit()

    def get_item(self, article: str, only_id: bool = False,) -> \
            Union[int, tuple[str, str, int, Union[int, None]]]:
        """Взятие товара из БД"""
        result = self.cursor.execute(
            "SELECT * FROM 'items' WHERE article = ?", (article,)
        )
        r = result.fetchone()
        if only_id:
            return r[0]
        return r[2], r[4], r[6], r[7]

    def exists_users_item(self, user_id: int, item_id: int) -> bool:
        """Проверка наличия актикула для пользователя в БД"""
        result = self.cursor.execute(
            "SELECT * FROM 'users_item' WHERE user_id = ? AND item_id = ?",
            (user_id, item_id)
        )
        return bool(result.fetchone())

    def add_users_item(self, user_id: int, item_id: int) -> None:
        """Добавление артикула для пользователя в БД"""
        self.cursor.execute(
            "INSERT INTO 'users_item' ('user_id', 'item_id') VALUES (?, ?)",
            (user_id, item_id)
        )
        return self.connect.commit()

    def get_users_item(self, item_id):
        result = self.cursor.execute(
            "SELECT user_id FROM 'users_item' WHERE item_id = ?", (item_id,)
        )
        return result.fetchall()

    def get_items_urls(self) -> list[int, str, str, str,
                                     int, Union[int, None]]:
        """Получение данных для парсера"""
        result = self.cursor.execute(
            "SELECT id, title, url, api_url, price, sale_price FROM 'items'"
        )
        return result.fetchall()

    def update_item(self, item_id: int, price: int, sale_price: int) -> None:
        """Изменение цены предмета"""
        self.cursor.execute(
            "UPDATE 'items' SET price = ?, sale_price=? WHERE id = ?",
            (price, sale_price, item_id)
        )
        return self.connect.commit()

    def close(self) -> NoReturn:
        """Закрытие БД"""
        self.connect.close()


# db = ConnectDB('../database.db')
# print(db.update_item(9, 999, 599))
