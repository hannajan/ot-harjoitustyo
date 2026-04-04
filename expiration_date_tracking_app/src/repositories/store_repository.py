from database_connection import get_database_connection

from entities.store import Store


def get_store_by_row(row):
    if row:
        return Store(
            store_id=row["store_id"],
            name=row["name"],
            owner_id=row["owner_id"]
        )

    return None


class StoreRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, store):
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO stores (store_id, name, owner_id) VALUES (?, ?, ?)",
            (store.store_id, store.name, store.owner_id)
        )

        self._connection.commit()

        return store


store_repository = StoreRepository(get_database_connection())
