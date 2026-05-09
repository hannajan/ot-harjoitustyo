from datetime import date, datetime, timedelta

from entities.product import Product
from entities.tracked_product import TrackedProduct

from repositories.product_repository import (
    product_repository as default_product_repository
)

from repositories.tracked_product_repository import (
    tracked_product_repository as default_tracked_product_repository
)

from repositories.department_repository import (
    department_repository as default_department_repository
)

from repositories.shelf_repository import (
    shelf_repository as default_shelf_repository
)


class ProductService:
    """Luokka, joka vastaa tuotteisiin liittyvästä sovelluslogiikasta.
    """

    def __init__(
        self,
        product_repository=default_product_repository,
        tracked_product_repository=default_tracked_product_repository,
        department_repository=default_department_repository,
        shelf_repository=default_shelf_repository
    ):
        """Luokan konstruktori.

        Args:
            product_repository: 
                ProductRepository-olio, joka vastaa tuotetietoihin 
                liittyvistä tietokantaoperaatioista.
            tracked_product_repository: 
                TrackedProductRepository-olio, joka vastaa seurannassa olevien tuotteiden
                tiekantaoperaatioista.
            department_repository: 
                DepartmentRepository-olio, joka vastaa osastoihin 
                liittyvistä tietokantaoperaatioista.
            shelf_repository: 
                ShelfReposiotry-olio, joka vastaa hyllyihin 
                liittyvistä tietokantaoperaatioista.
        """
        self._product_repository = product_repository
        self._tracked_product_repository = tracked_product_repository
        self._department_repository = department_repository
        self._shelf_repository = shelf_repository

    def add_product_info(self, ean_code, name):
        """Lisää tuotteen tietokantaan.

        Args:
            ean_code: Merkkijono, joka on tuotteen yksilöivä EAN-koodi.
            name: Merkkijono, joka on tuotteen nimi.

        Raises:
            ValueError, jos EAN-koodia ei ole annettu.
            ValueError, jos tuotteen nimeä ei ole annettu.

        Returns:
            _type_: _description_
        """
        if not ean_code:
            raise ValueError("Product EAN-code must be given")

        if not name:
            raise ValueError("Product name must be given")

        product = Product(ean_code=ean_code, name=name)

        self._product_repository.create(product=product)

        return product

    def get_tracked_products_for_shelf(self, shelf_id):
        """Palauttaa listan TrackedProduct-olioita hyllyn id:n perusteella.

        Args:
            shelf_id: 
                Merkkijono, joka on sen hyllyn id, 
                jonka seurannassa olevat tuotteet palautetaan.

        Returns:
            Lista TrackedProduct-olioita.
        """
        return self._tracked_product_repository.get_by_shelf_id(shelf_id)

    def find_product_by_ean(self, ean_code):
        """Palauttaa EAN-koodin perusteella löydetyn tuotteen.

        Args:
            ean_code: Merkkijono, joka on tuotteen yksilöivä EAN-koodi.

        Raises:
            ValueError, jos EAN-koodia ei ole annettu.

        Returns:
            Product-olion.
        """
        if not ean_code:
            raise ValueError("EAN-code must be given")

        product = self._product_repository.get_by_ean_code(ean_code)
        return product

    def add_tracked_product(self, ean_code, expiration_date, shelf_id):
        """Lisää tuotteen seurantaan.

        Args:
            ean_code: Merkkijono, joka on seurantaan lisättävän tuotteen EAN-koodi.
            expiration_date: kuusinumeroinen (ppkkvv) parasta ennen -päiväystä kuvaava merkkijono.
            shelf_id: Merkkijono, joka on hyllyn yksilöivä id.

        Raises:
            ValueError, jos EAN-koodia ei ole annettu.
            ValueError, jos parasta ennen-päiväystä ei ole annettu.
            ValueError, jos hyllyn id:tä ei ole annettu.
            ValueError, jos parasta ennen -päiväys ei ole kuusinumeroinen luku.
            ValueError, jos päiväyksen parsiminen ei onnistu.

        Returns:
            TrackedProduct-olion, joka luotiin.
        """
        if not ean_code:
            raise ValueError("EAN code must be given")

        if not expiration_date:
            raise ValueError("Expiration date must be given")

        if not shelf_id:
            raise ValueError("Shelf id must be given")

        if len(expiration_date) != 6 or not expiration_date.isdigit():
            raise ValueError("Date must be in format ddmmyy")

        try:
            exp_date = datetime.strptime(expiration_date, "%d%m%y").date()
        except ValueError as exc:
            raise ValueError("Invalid date") from exc

        tracked_product = TrackedProduct(
            ean_code=ean_code,
            expiration_date=exp_date,
            shelf_id=shelf_id,
        )

        self._tracked_product_repository.create(tracked_product)

        return tracked_product

    def update_tracked_product_date(self, tracked_product_id, new_expiration_date):
        """Päivittää seurannassa olevan tuotteen parasta ennen -päiväyksen.

        Args:
            tracked_product_id: Merkkijono, joka on päivitettävän tuotteen id.
            new_expiration_date: Kuusinumeroinen merkkijono (ppkkvv), joka on uusi päiväys.

        Raises:
            ValueError, jos tuotteen id:tä ei ole annettu.
            ValueError, jos parasta ennen -päiväystä ei ole annettu.
            ValueError, jos parasta ennen -päiväys ei ole kuusinumeroinen luku
            ValueError, jos päiväyksen parsiminen ei onnistu.
        """
        if not tracked_product_id:
            raise ValueError("Tracked product id must be given")

        if not new_expiration_date:
            raise ValueError("Expiration date must be given")

        if len(new_expiration_date) != 6 or not new_expiration_date.isdigit():
            raise ValueError("Date must be in format ddmmyy")

        try:
            parsed_date = datetime.strptime(
                new_expiration_date, "%d%m%y").date()
        except ValueError as exc:
            raise ValueError("Date format must be ddmmyy") from exc

        self._tracked_product_repository.update_expiration_date(
            tracked_product_id=tracked_product_id,
            expiration_date=parsed_date.isoformat()
        )

    def delete_tracked_product(self, tracked_product_id):
        """Poistaa tuotteen seurannasta.

        Args:
            tracked_product_id: Merkkijono, joka on poistettavan tuotteen id.

        Raises:
            ValueError, jos id:tä ei ole annettu.
        """
        if not tracked_product_id:
            raise ValueError("Tracked product id must be given")

        self._tracked_product_repository.delete(tracked_product_id)

    # tämän metodin runko on generoitu tekoälyllä
    def get_products_to_check_by_shelf(self, shelf_id):
        """Palauttaa tarkistettavat tuotteen hyllyn id:n perusteella.

        Args:
            shelf_id: Merkkijono, joka on hyllyn id.

        Returns:
            Lista TrackedProduct-olioita.
        """
        products = self._tracked_product_repository.get_by_shelf_id(shelf_id)
        shelf = self._shelf_repository.get_by_id(shelf_id)
        department = self._department_repository.get_by_id(shelf.department_id)

        today = date.today()
        products_to_check = []

        for product in products:
            check_days = product.check_days_before

            if check_days is None:
                check_days = department.check_days_before

            expiration_date = datetime.strptime(
                product.expiration_date, "%Y-%m-%d").date()

            check_date = expiration_date - timedelta(days=check_days)

            if check_date <= today:
                products_to_check.append(product)

        return products_to_check


product_service = ProductService()
