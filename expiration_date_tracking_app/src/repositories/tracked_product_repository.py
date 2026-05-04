from database_connection import get_database_connection

from entities.tracked_product import TrackedProduct


def get_tracked_product_by_row(row):
    if row:
        return TrackedProduct(
            tracked_product_id=row["tracked_product_id"],
            ean_code=row["ean_code"],
            expiration_date=row["expiration_date"],
            shelf_id=row["shelf_id"],
            check_days_before=row["check_days_before"]
        )
    return None


class TrackedProductRepository:
    """Luokka, joka vastaa TrackedProduct-olioihin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection: Connection-olio, joka on tietokantayhteys.
        """
        self._connection = connection

    def create(self, tracked_product):
        """Tallentaa seurannassa olevan tuotteen tietokantaan.

        Args:
            tracked_product: TrackedProduct-olio, joka on tietokantaan tallennettava tuote.

        Returns:
            Tietokantaan tallennettu TrackedProduct-olio.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO tracked_products "
            "(tracked_product_id, ean_code, expiration_date, shelf_id, check_days_before) "
            "VALUES (?, ?, ?, ?, ?) ",
            (
                tracked_product.tracked_product_id,
                tracked_product.ean_code,
                tracked_product.expiration_date,
                tracked_product.shelf_id,
                tracked_product.check_days_before)
        )

        self._connection.commit()

        return tracked_product

    def delete_all(self):
        """Poistaa kaikki seurannassa olevat tuotteet tietokannasta.
        """
        cursor = self._connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("DELETE FROM tracked_products")
        self._connection.commit()

    def delete(self, tracked_product_id):
        """Poistaa seurannassa olevan tuotteen tietokannasta.

        Args:
            tracked_product_id: Merkkijono, joka on poistettavan tuotteen id
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "DELETE FROM tracked_products WHERE tracked_product_id = ?",
            (tracked_product_id,)
        )

        self._connection.commit()

    def get_by_shelf_id(self, shelf_id):
        """Palauttaa listan seurannassa olevista tuotteista hyllyn id:n perusteella

        Args:
            shelf_id: Merkkijono, joka on sen hyllyn id, jonka tuotteet palautetaan

        Returns:
            Lista TrackedProduct-olioita
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT tracked_product_id, ean_code, expiration_date, shelf_id, check_days_before "
            "FROM tracked_products "
            "WHERE shelf_id = ? ",
            (shelf_id,)
        )

        rows = cursor.fetchall()

        return [get_tracked_product_by_row(row) for row in rows]

    # tämä metodi on generoitu tekoälyllä
    def get_by_shelf(self, shelf_id):
        """Palauttaa listan hyllyn id:n perusteella löydetyistä 
        seurannassa olevista tuotteista


        Args:
            shelf_id: Merkkijono, joka on sen hyllyn id,
            jonka tuotteet palautetaan

        Returns:
            Lista TrackedProduct-olioita
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT "
            "tracked_product_id, "
            "ean_code, "
            "expiration_date, "
            "shelf_id, "
            "check_days_before "
            "FROM tracked_products "
            "WHERE shelf_id = ?",
            (shelf_id,)
        )

        rows = cursor.fetchall()

        return [get_tracked_product_by_row(row) for row in rows]

    def update_expiration_date(self, tracked_product_id, expiration_date):
        """Päivittää seurannassa olevan tuotteen päiväyksen.

        Args:
            tracked_product_id: Merkkijono, joka on päivitettävän tuotteen id.
            expiration_date: ISO-date, joka on uusi päivitettävä päiväys
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "UPDATE tracked_products "
            "SET expiration_date = ? "
            "WHERE tracked_product_id = ?",
            (
                expiration_date,
                tracked_product_id
            )
        )

        self._connection.commit()


tracked_product_repository = TrackedProductRepository(
    get_database_connection())
