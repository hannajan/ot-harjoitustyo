from database_connection import get_database_connection
from entities.shelf import Shelf


def get_shelf_by_row(row):
    if row:
        return Shelf(
            shelf_id=row["shelf_id"],
            department_id=row["department_id"],
            name=row["name"],
            is_default=row["is_default"]
        )
    return None


class ShelfRepository:
    """Luokka, joka vastaa hyllyihin liittyvistä tietokantaoperaatioista
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection: Connection-olio, joka on tietokantayhteys.
        """
        self._connection = connection

    def create(self, shelf):
        """Tallentaa hyllyn tietokantaan.

        Args:
          shelf: Shelf-olio, joka tallentetaan tietokantaan.
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO shelves (shelf_id, department_id, name, is_default)
            VALUES (?, ?, ?, ?)
        """, (
            shelf.shelf_id,
            shelf.department_id,
            shelf.name,
            int(shelf.is_default)
        ))
        self._connection.commit()

    def get_shelves_by_department(self, department_id):
        """Palauttaa osaston hyllyt.

        Args:
          department_id: Merkkijono, joka viittaa osastoon, jonka hyllyt palautetaan.

        Returns:
          Lista Shelf-olioita.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM shelves WHERE department_id = ? ",
            (department_id,))

        rows = cursor.fetchall()

        return [get_shelf_by_row(row) for row in rows]

    def create_default_shelf(self, department_id):
        """Luo oletusarvohyllyn uudelle osastolle.

        Args:
            department_id: Merkkijono, joka viittaa luotuun osastoon, jolle oletusarvohylly luodaan.
        """
        shelf = Shelf(
            department_id=department_id,
            name="Shelf 1",
            is_default=True
        )
        self.create(shelf)

    def update(self, shelf):
        """Päivittää Shelf-olion tiedot tietokantaan.

        Args:
            shelf: hylly, jonka tiedot päivitetään tietokantaan.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "UPDATE shelves "
            "SET name = ?, is_default = ? "
            "WHERE shelf_id = ? ",
            (
                shelf.name,
                int(shelf.is_default),
                shelf.shelf_id
            ))

        self._connection.commit()


shelf_repository = ShelfRepository(get_database_connection())
