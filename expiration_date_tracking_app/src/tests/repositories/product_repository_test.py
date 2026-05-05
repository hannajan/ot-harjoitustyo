import unittest

from entities.product import Product
from repositories.product_repository import product_repository

class TestProductRepository(unittest.TestCase):
    def setUp(self):
        product_repository.delete_all()

        product_repository.create(Product("6419800120018", "Teho energiajuoma"))
    
    def test_create_product_works(self):
        juice = Product("6415130027980", "Marli Juissi sekamehujuoma 1l")

        product = product_repository.create(juice)

        self.assertEqual(product.name, "Marli Juissi sekamehujuoma 1l")
        self.assertEqual(product.ean_code, "6415130027980")

    def test_get_by_ean_code_works(self):
        product = product_repository.get_by_ean_code("6419800120018")

        self.assertEqual(product.name, "Teho energiajuoma")