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
    def __init__(
        self,
        product_repository=default_product_repository,
        tracked_product_repository=default_tracked_product_repository,
        department_repository=default_department_repository,
        shelf_repository=default_shelf_repository
    ):
        self._product_repository = product_repository
        self._tracked_product_repository = tracked_product_repository
        self._department_repository = department_repository
        self._shelf_repository = shelf_repository

    def add_product_info(self, ean_code, name):
        if not ean_code:
            raise ValueError("Product EAN-code must be given")

        if not name:
            raise ValueError("Product name must be given")

        product = Product(ean_code=ean_code, name=name)

        self._product_repository.create(product=product)

        return product

    def get_tracked_products_for_shelf(self, shelf_id):
        return self._tracked_product_repository.get_by_shelf_id(shelf_id)

    def find_product_by_ean(self, ean_code):
        if not ean_code:
            raise ValueError("EAN-code must be given")

        product = self._product_repository.get_by_ean_code(ean_code)
        return product

    def add_tracked_product(self, ean_code, expiration_date, shelf_id):
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
            raise ValueError("Date must be given in format ddmmyy") from exc

        tracked_product = TrackedProduct(
            ean_code=ean_code,
            expiration_date=exp_date,
            shelf_id=shelf_id,
        )

        self._tracked_product_repository.create(tracked_product)

        return tracked_product

    def update_tracked_product_date(self, tracked_product_id, new_expiration_date):
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
        if not tracked_product_id:
            raise ValueError("Tracked product id must be given")

        self._tracked_product_repository.delete(tracked_product_id)

    def get_products_to_check_by_department(self, department_id):
        products = self._tracked_product_repository.get_by_department(
            department_id)
        department = self._department_repository.get_by_id(department_id)

        today = date.today()
        result = []

        for product in products:
            expiration_date = datetime.strptime(
                product.expiration_date, "%Y-%m-%d").date()

            check_days_before = product.check_days_before

            if check_days_before is None:
                check_days_before = department.check_days_before

            check_date = expiration_date - timedelta(days=check_days_before)

            if check_date <= today:
                result.append(product)

        return result

    def get_products_to_check_by_shelf(self, shelf_id):
        products = self._tracked_product_repository.get_by_shelf(shelf_id)
        shelf = self._shelf_repository.get_by_id(shelf_id)
        department = self._department_repository.get_by_id(shelf.department_id)

        today = date.today()
        result = []

        for p in products:
            check_days = p.check_days_before

            if check_days is None:
                check_days = department.check_days_before

            expiration_date = datetime.strptime(
                p.expiration_date, "%Y-%m-%d").date()

            check_date = expiration_date - timedelta(days=check_days)

            if check_date <= today:
                result.append(p)

        return result


product_service = ProductService()
