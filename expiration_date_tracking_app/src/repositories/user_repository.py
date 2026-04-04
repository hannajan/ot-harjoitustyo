from database_connection import get_database_connection

from entities.user import User


def get_user_by_row(row):
    if row:
        return User(
            user_id=row["user_id"],
            username=row["username"],
            password_hash=row["password_hash"],
            role=row["role"]
        )

    return None


class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, user):
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO users (user_id, username, password_hash, role) VALUES (?, ?, ?, ?)",
            (user.user_id, user.username, user.password_hash, user.role)
        )

        self._connection.commit()

        return user

    def delete_all(self):
        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM users")
        self._connection.commit()

    def get_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()

        return list(map(get_user_by_row, rows))

    def find_by_username(self, username):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        row = cursor.fetchone()

        return get_user_by_row(row)

    def get_user_by_id(self, user_id):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )

        row = cursor.fetchone()

        return get_user_by_row(row)


user_repository = UserRepository(get_database_connection())
