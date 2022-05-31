import sqlite3
from typing import Tuple, List, Union


class DataBaseModel:
    """Класс БД. Содержит методы обращения к БД"""

    """Методы обращения к таблице profile"""

    @classmethod
    def insert_user(cls, user_tuple: Tuple) -> None:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO 'app_i_want_profile' (user_id, username, role) "
                "VALUES (?, ?, ?)", user_tuple
            )

    @classmethod
    def select_check_user(cls, user_id, role) -> bool:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id FROM 'app_i_want_profile' "
                "WHERE user_id=? AND role=?;", (user_id, role)
            )
            exists = cursor.fetchone()
            if exists:
                return True
            else:
                return False

    @classmethod
    def select_resp_username(cls, user_id: int) -> Union[List, None]:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username FROM 'app_i_want_profile' WHERE user_id = ? and role='Я исполнитель'", (user_id,)
            )
            result = cursor.fetchone()
            return result

    """Методы обращения к таблице task"""

    @classmethod
    def insert_task(cls, task_tuple: Tuple) -> None:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO 'app_i_want_task' (user_id, title, price, category, status) "
                "VALUES (?, ?, ?, ?, ?)", task_tuple
            )

    @classmethod
    def select_my_task(cls, user_id: int) -> List:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, price FROM 'app_i_want_task' WHERE user_id=?", (user_id,))
            result = cursor.fetchall()
            return result

    @classmethod
    def delete_task(cls, task_id: int) -> None:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM 'app_i_want_task' WHERE id = ?;", (task_id,)
            )

    @classmethod
    def select_all_task(cls) -> Union[List, None]:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM 'app_i_want_task'"
            )
            result = cursor.fetchall()
            return result

    @classmethod
    def select_task_my_resp(cls, task_id: int) -> Union[List, None]:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title, price FROM 'app_i_want_task' WHERE id = ?", (task_id,)
            )
            result = cursor.fetchone()
            return result

    @classmethod
    def select_limit_task(cls, index: int, limit: int) -> Union[List, None]:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM 'app_i_want_task' LIMIT ?, ?", (index, limit)
            )
            result = cursor.fetchall()
            return result

    """Методы обращения к таблице taskresp"""

    @classmethod
    def insert_task_resp(cls, task_resp_tuple: Tuple) -> None:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO 'app_i_want_taskresp' (user_id, username, task_id, resp_text) "
                "VALUES (?, ?, ?, ?)", task_resp_tuple
            )

    @classmethod
    def delete_task_resp(cls, task_id: int) -> None:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM 'app_i_want_taskresp' WHERE task_id=?", (task_id, )
            )

    @classmethod
    def select_task_resp(cls, task_id: int) -> Union[List, None]:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, resp_text FROM 'app_i_want_taskresp' WHERE task_id = ?", (task_id,)
            )
            result = cursor.fetchall()
            return result

    @classmethod
    def select_count_task_resp(cls, task_id: int) -> Union[List, None]:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM 'app_i_want_taskresp' WHERE task_id = ?", (task_id,)
            )
            result = cursor.fetchone()
            return result

    @classmethod
    def select_task_id_resp(cls, user_id) -> Union[List, None]:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM 'app_i_want_taskresp' WHERE user_id=?", (user_id,)
            )
            result = cursor.fetchall()
            return result

    """Методы обращения к таблице botmessage"""

    @classmethod
    def insert_bot_message(cls, chat: int, message: int) -> None:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO 'app_i_want_botmessage' (chat, message) "
                "VALUES (?, ?)", (chat, message)
            )

    @classmethod
    def select_bot_message(cls, user_id: int) -> Union[List, None]:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM 'app_i_want_botmessage' WHERE chat=?", (user_id,)
            )
            result = cursor.fetchall()
            return result

    @classmethod
    def delete_bot_message(cls, user_id: int) -> None:
        with sqlite3.connect('../i_want_admin/db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM 'app_i_want_botmessage' WHERE chat=?", (user_id, )
            )
