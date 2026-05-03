from database_connection import get_database_connection

from entities.product import Product


def get_product_by_row(row):
    if row:
        return Product(
            ean_code=row["ean_code"],
            name=row["name"]
        )
    return None


class ProductRepository:
    """Luokka, joka vastaa Product-olioihin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection: Connection-olio, joka on tietokantayhteys.
        """
        self._connection = connection

    def create(self, product):
        """Tallentaa tuotteen tietokantaan.

        Args:
            product: Product-olio, joka on tietokantaan tallennettava tuote.

        Returns:
            Tietokantaan tallennettu Product-olio.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO products "
            "(ean_code, name) "
            "VALUES (?, ?) ",
            (
                product.ean_code,
                product.name,
            )
        )

        self._connection.commit()

        return product

    def delete_all(self):
        """Poistaa kaikki tuotteet tietokannasta.
        """
        cursor = self._connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("DELETE FROM products")
        self._connection.commit()

    def get_by_ean_code(self, ean_code):
        """Hakee tuotteen EAN-koodin perusteella.

        Args:
            ean_code: Merkkijono, joka on tuotteen EAN-koodi.

        Returns:
            Product-olio, jos tuote löytyy.
            None, jos tuotetta ei löydy tietokannasta.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT ean_code, name FROM products WHERE ean_code = ?",
            (ean_code,)
        )

        row = cursor.fetchone()

        return get_product_by_row(row)


product_repository = ProductRepository(
    get_database_connection())
