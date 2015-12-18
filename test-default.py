from django.test import TestCase
from decimal import Decimal
from shop.models import Product


class AnimalTestCase(TestCase):
    def setUp(self):
        Product.objects.create(
            name="Dan",
            description="Whateva",
            current_price=Decimal("3.44"),
            thumbnail_filename="asd",
            image_filename="asd",
            is_active=True
        )

    def test_create(self):
        dan = Product.objects.get(name="Dan")
        self.assertEqual(dan.name, "Dan")

