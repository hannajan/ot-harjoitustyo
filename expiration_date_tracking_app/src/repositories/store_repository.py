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
    """Luokka, joka vastaa Store-olioihin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection: Connection-olio, joka on tietokantayhteys.
        """
        self._connection = connection

    def create(self, store):
        """Tallentaa kaupan tietokantaan.

        Args:
            store: Store-olio, joka on tietokantaan tallennettava kauppa.

        Returns:
            Tietokantaan tallennettu Store-olio.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO stores (store_id, name, owner_id) VALUES (?, ?, ?)",
            (store.store_id, store.name, store.owner_id)
        )

        self._connection.commit()

        return store

    def find_by_id(self, store_id):
        """Palauttaa id:n perusteella löydetyn kaupan.

        Args:
            store_id: Merkkijono, joka on palautettavan kaupan id.

        Returns:
            Store-olio, joka on löydetty id:n perusteella.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM stores WHERE store_id = ?",
            (store_id,)
        )

        row = cursor.fetchone()

        return get_store_by_row(row)

    def find_all_by_owner_id(self, owner_id):
        """Palauttaa kaikki kauppiaan omistamat kaupat.

        Args:
            owner_id: Merkkijono, joka on sen kauppiaan id, jonka kaupat palautetaan.

        Returns:
            Lista Store-olioita.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM stores WHERE owner_id = ?",
            (owner_id,)
        )

        rows = cursor.fetchall()

        return [get_store_by_row(row) for row in rows]

    def delete_all(self):
        """Poistaa kaikki kaupat tietokannasta.
        """
        cursor = self._connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("DELETE FROM stores")
        self._connection.commit()

    def get_all(self):
        """Palauttaa kaikki kaupat.

        Returns:
            Lista Store-olioita.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM stores"
        )

        rows = cursor.fetchall()

        return [get_store_by_row(row) for row in rows]


store_repository = StoreRepository(get_database_connection())
