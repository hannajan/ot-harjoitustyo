import unittest

from services.product_service import ProductService

from entities.product import Product
from entities.tracked_product import TrackedProduct


class MockProductRepository:
    def __init__(self, products=None):
        self.products = products or []

    def create(self, product):
        self.products.append(product)


class MockTrackedProductRepository:
    def __init__(self, tracked_products=None):
        self.tracked_products = tracked_products or []

    def create(self, tracked_product):
        self.tracked_products.append(tracked_product)

    def update_expiration_date(self, tracked_product_id, expiration_date):
        for tracked_product in self.tracked_products:
            if tracked_product.tracked_product_id == tracked_product_id:
                tracked_product.expiration_date = expiration_date

    def get_by_shelf_id(self, shelf_id):
        products = []

        for self.tracked_product in self.tracked_products:
            if self.tracked_product.shelf_id == shelf_id:
                products.append(self.tracked_product)

        return products


class MockDepartmentRepository:
    def __init__(self):
        pass


class MockShelfRepository:
    def __init__(self):
        pass


class TestProductService(unittest.TestCase):
    def setUp(self):
        self.product_service = ProductService(
            product_repository=MockProductRepository(),
            tracked_product_repository=MockTrackedProductRepository(),
            department_repository=MockDepartmentRepository(),
            shelf_repository=MockShelfRepository()
        )

    def test_add_product_info_works_with_valid_attributes(self):
        product = self.product_service.add_product_info(
            ean_code="123456", name="Maito")

        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, "Maito")
        self.assertEqual(product.ean_code, "123456")

    def test_add_product_info_raises_valueerror_if_ean_missing(self):
        with self.assertRaisesRegex(ValueError, "EAN-code must be given"):
            self.product_service.add_product_info(ean_code=None, name="Sipuli")

    def test_add_product_info_raises_valueerror_if_name_missing(self):
        with self.assertRaisesRegex(ValueError, "Product name must be given"):
            self.product_service.add_product_info(ean_code="456456", name=None)

    def test_add_tracked_product_works_with_valid_attributes(self):
        tracked_product = self.product_service.add_tracked_product(
            ean_code="654321",
            expiration_date="110626",
            shelf_id="id123"
        )

        self.assertIsInstance(tracked_product, TrackedProduct)

    def test_add_tracked_product_raises_error_if_ean_code_missing(self):
        with self.assertRaisesRegex(ValueError, "EAN code must be given"):
            self.product_service.add_tracked_product(
                ean_code=None,
                expiration_date="230526",
                shelf_id="id123"
            )

    def test_add_tracked_product_raises_error_if_expiration_date_missing(self):
        with self.assertRaisesRegex(ValueError, "Expiration date must be given"):
            self.product_service.add_tracked_product(
                ean_code="998877",
                expiration_date=None,
                shelf_id="id123"
            )

    def test_add_tracked_product_raises_error_with_invalid_expiration_date(self):
        with self.assertRaisesRegex(ValueError, "Date must be in format ddmmyy"):
            self.product_service.add_tracked_product(
                ean_code="998877",
                expiration_date="28092026",
                shelf_id="id123"
            )

        with self.assertRaisesRegex(ValueError, "Invalid date"):
            self.product_service.add_tracked_product(
                ean_code="998877",
                expiration_date="320926",
                shelf_id="id123"
            )

    def test_add_tracked_product_raises_error_if_shelf_id_missing(self):
        with self.assertRaisesRegex(ValueError, "Shelf id must be given"):
            self.product_service.add_tracked_product(
                ean_code="998877",
                expiration_date="220727",
                shelf_id=None
            )

    def test_update_tracked_product_date_works(self):
        tracked_product = self.product_service.add_tracked_product(
            "123456", "070726", "id123")
        self.product_service.update_tracked_product_date(
            tracked_product_id=tracked_product.tracked_product_id,
            new_expiration_date="111127"
        )

        products = self.product_service.get_tracked_products_for_shelf(
            shelf_id="id123")

        self.assertEqual(products[0].ean_code, "123456")
        self.assertEqual(products[0].expiration_date, "2027-11-11")
        self.assertNotEqual(products[0].expiration_date, "2026-07-07")
