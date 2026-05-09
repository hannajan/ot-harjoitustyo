import unittest

from entities.merchant import Merchant
from entities.store import Store
from entities.department import Department
from entities.shelf import Shelf
from entities.product import Product
from entities.tracked_product import TrackedProduct

from repositories.permission_repository import permission_repository
from repositories.shelf_repository import shelf_repository
from repositories.store_repository import store_repository
from repositories.user_repository import user_repository
from repositories.department_repository import department_repository
from repositories.tracked_product_repository import (
    tracked_product_repository,
    get_tracked_product_by_row
)
from repositories.product_repository import product_repository


class TestTrackedProductRepository(unittest.TestCase):
    def setUp(self):
        permission_repository.delete_all()
        product_repository.delete_all()
        tracked_product_repository.delete_all()
        shelf_repository.delete_all()
        department_repository.delete_all()
        store_repository.delete_all()
        user_repository.delete_all()

        user = user_repository.create(Merchant("kauppias", "salasana"))
        store = store_repository.create(Store("Kauppa", user.user_id))
        department = department_repository.create(
            Department(store.store_id, "Osasto", 2))
        self.shelf = shelf_repository.create(
            Shelf(department.department_id, "Hylly"))
        product_repository.create(Product("123456", "Mehu"))
        self.tracked_product = tracked_product_repository.create(TrackedProduct(
            ean_code="567567", expiration_date="2026-05-09", shelf_id=self.shelf.shelf_id))

    def test_create_tracked_product_works(self):
        tracked_product = tracked_product_repository.create(TrackedProduct(
            ean_code="123456", expiration_date="2026-05-05", shelf_id=self.shelf.shelf_id))

        self.assertEqual(tracked_product.ean_code, "123456")

    def test_delete_works(self):
        tracked_product = tracked_product_repository.create(TrackedProduct(
            ean_code="123456", expiration_date="2026-05-05", shelf_id=self.shelf.shelf_id))
        tracked_product_repository.delete(tracked_product.tracked_product_id)

        products = tracked_product_repository.get_by_shelf_id(
            self.shelf.shelf_id)

        self.assertEqual(len(products), 1)

    def test_update_expiration_date_works(self):
        products = tracked_product_repository.get_by_shelf_id(
            self.shelf.shelf_id)
        self.assertEqual(products[0].expiration_date, "2026-05-09")

        tracked_product_repository.update_expiration_date(
            self.tracked_product.tracked_product_id, "2026-05-19")

        products = tracked_product_repository.get_by_shelf_id(
            self.shelf.shelf_id)
        self.assertEqual(products[0].expiration_date, "2026-05-19")
        self.assertNotEqual(products[0].expiration_date, "2026-05-09")

    def test_returns_empty_list_if_shelf_id_doesnt_exist(self):
        products = tracked_product_repository.get_by_shelf_id("nonexistant123")

        self.assertEqual(len(products), 0)

    def test_get_tracked_product_by_row_returns_none_if_row_no_row(self):
        product = get_tracked_product_by_row(None)

        self.assertIsNone(product)
