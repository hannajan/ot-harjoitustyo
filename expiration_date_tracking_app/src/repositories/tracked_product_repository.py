from database_connection import get_database_connection

from entities.tracked_product import TrackedProduct


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
            "(id, ean_code, expiration_date, shelf_id, check_days_before) "
            "VALUES (?, ?, ?, ?, ?) ",
            (
                tracked_product.id,
                tracked_product.ean_code,
                tracked_product.expiration_date,
                tracked_product.shelf_id,
                tracked_product.check_days_before)
        )

        self._connection.commit()

        return tracked_product


tracked_product_repository = TrackedProductRepository(
    get_database_connection())
