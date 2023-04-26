from product import Coffee, Tea
import unittest
from marketplace import Marketplace


class TestMarketPlace(unittest.TestCase):

    def setUp(self):
        """
        Sets up a mock marketplace with a queue of size 10 for producers
        """
        self.marketplace = Marketplace(10)

        self.first_product = Coffee("Brasil", 1, "5.09", "MEDIUM")
        self.second_product = Tea("Wild Cherry", 4, "Wild Cherry")

    def test_register_producer(self):
        """
        Tests if the registered producers get the correct ids
        """
        self.assertEqual(self.marketplace.register_producer(), 0)
        self.assertEqual(self.marketplace.register_producer(), 1)
        self.assertEqual(self.marketplace.register_producer(), 2)

    def test_publish(self):

        producer = self.marketplace.register_producer()

        """
        Tests if multiple products are correctly published to marketplace
        and the number of products/ producer is increased
        """
        self.marketplace.publish(producer, self.first_product)
        self.assertEqual(self.marketplace.producers_list[producer], 1)
        self.assertIn({'id': producer, 'product': self.first_product}, self.marketplace.products_list)
        self.marketplace.publish(producer, self.second_product)
        self.assertEqual(self.marketplace.producers_list[producer], 2)
        self.assertIn({'id': producer, 'product': self.second_product}, self.marketplace.products_list)

    def test_new_cart(self):
        """
        Tests if the first four new carts get the correct ids
        """
        self.assertEqual(self.marketplace.new_cart(), 0)
        self.assertEqual(self.marketplace.new_cart(), 1)

    def test_add_to_cart(self):
        """
        Tests if the products are added to the cart correctly
        """

        producer = self.marketplace.register_producer()
        cart = self.marketplace.new_cart()

        self.marketplace.publish(producer, self.first_product)
        self.marketplace.publish(producer, self.second_product)

        self.marketplace.add_to_cart(cart, self.first_product)

        self.assertNotIn({'id': producer, 'product': self.first_product}, self.marketplace.products_list)
        self.assertEqual(self.marketplace.producers_list[producer], 1)
        self.assertIn({'id': producer, 'product': self.first_product}, self.marketplace.carts_list[cart])

        self.marketplace.add_to_cart(cart, self.second_product)

        self.assertNotIn({'id': producer, 'product': self.second_product}, self.marketplace.products_list)
        self.assertEqual(self.marketplace.producers_list[producer], 0)
        self.assertIn({'id': producer, 'product': self.second_product}, self.marketplace.carts_list[cart])

    def test_remove_from_cart(self):
        """
        Tests if the products are added to the cart correctly
        """
        producer = self.marketplace.register_producer()
        cart = self.marketplace.new_cart()

        self.marketplace.publish(producer, self.first_product)
        self.marketplace.publish(producer, self.second_product)

        self.marketplace.add_to_cart(cart, self.first_product)
        self.marketplace.add_to_cart(cart, self.second_product)

        self.marketplace.remove_from_cart(cart, self.first_product)
        self.assertIn({'id': producer, 'product': self.first_product}, self.marketplace.products_list)
        self.assertNotIn({'id': producer, 'product': self.first_product}, self.marketplace.carts_list[cart])
        self.assertEqual(self.marketplace.producers_list[producer], 1)

        self.marketplace.remove_from_cart(cart, self.second_product)
        self.assertIn({'id': producer, 'product': self.second_product}, self.marketplace.products_list)
        self.assertNotIn({'id': producer, 'product': self.second_product}, self.marketplace.carts_list[cart])
        self.assertEqual(self.marketplace.producers_list[producer], 2)

    def test_place_order(self):
        """
        Tests if place order returns the expected products
        """
        first_product = Coffee("Brasil", 1, "5.09", "MEDIUM")
        second_product = Tea("Wild Cherry", 4, "Wild Cherry")
        producer = self.marketplace.register_producer()
        cart = self.marketplace.new_cart()

        self.marketplace.publish(producer, first_product)
        self.marketplace.publish(producer, second_product)

        self.marketplace.add_to_cart(cart, first_product)
        self.marketplace.add_to_cart(cart, second_product)

        ordered_products = self.marketplace.place_order(cart)

        self.assertEqual(ordered_products[0], first_product)
        self.assertEqual(ordered_products[1], second_product)
class TestMarketPlace(unittest.TestCase):

    def setUp(self):
        """
        Sets up a mock marketplace with a queue of size 10 for producers
        """
        self.marketplace = Marketplace(10)

        self.first_product = Coffee("Brasil", 1, "5.09", "MEDIUM")
        self.second_product = Tea("Wild Cherry", 4, "Wild Cherry")

    def test_register_producer(self):
        """
        Tests if the registered producers get the correct ids
        """
        self.assertEqual(self.marketplace.register_producer(), 0)
        self.assertEqual(self.marketplace.register_producer(), 1)
        self.assertEqual(self.marketplace.register_producer(), 2)

    def test_publish(self):

        producer = self.marketplace.register_producer()

        """
        Tests if multiple products are correctly published to marketplace
        and the number of products/ producer is increased
        """
        self.marketplace.publish(producer, self.first_product)
        self.assertEqual(self.marketplace.producers_list[producer], 1)
        self.assertIn({'id': producer, 'product': self.first_product}, self.marketplace.products_list)
        self.marketplace.publish(producer, self.second_product)
        self.assertEqual(self.marketplace.producers_list[producer], 2)
        self.assertIn({'id': producer, 'product': self.second_product}, self.marketplace.products_list)

    def test_new_cart(self):
        """
        Tests if the first four new carts get the correct ids
        """
        self.assertEqual(self.marketplace.new_cart(), 0)
        self.assertEqual(self.marketplace.new_cart(), 1)

    def test_add_to_cart(self):
        """
        Tests if the products are added to the cart correctly
        """

        producer = self.marketplace.register_producer()
        cart = self.marketplace.new_cart()

        self.marketplace.publish(producer, self.first_product)
        self.marketplace.publish(producer, self.second_product)

        self.marketplace.add_to_cart(cart, self.first_product)

        self.assertNotIn({'id': producer, 'product': self.first_product}, self.marketplace.products_list)
        self.assertEqual(self.marketplace.producers_list[producer], 1)
        self.assertIn({'id': producer, 'product': self.first_product}, self.marketplace.carts_list[cart])

        self.marketplace.add_to_cart(cart, self.second_product)

        self.assertNotIn({'id': producer, 'product': self.second_product}, self.marketplace.products_list)
        self.assertEqual(self.marketplace.producers_list[producer], 0)
        self.assertIn({'id': producer, 'product': self.second_product}, self.marketplace.carts_list[cart])

    def test_remove_from_cart(self):
        """
        Tests if the products are added to the cart correctly
        """
        producer = self.marketplace.register_producer()
        cart = self.marketplace.new_cart()

        self.marketplace.publish(producer, self.first_product)
        self.marketplace.publish(producer, self.second_product)

        self.marketplace.add_to_cart(cart, self.first_product)
        self.marketplace.add_to_cart(cart, self.second_product)

        self.marketplace.remove_from_cart(cart, self.first_product)
        self.assertIn({'id': producer, 'product': self.first_product}, self.marketplace.products_list)
        self.assertNotIn({'id': producer, 'product': self.first_product}, self.marketplace.carts_list[cart])
        self.assertEqual(self.marketplace.producers_list[producer], 1)

        self.marketplace.remove_from_cart(cart, self.second_product)
        self.assertIn({'id': producer, 'product': self.second_product}, self.marketplace.products_list)
        self.assertNotIn({'id': producer, 'product': self.second_product}, self.marketplace.carts_list[cart])
        self.assertEqual(self.marketplace.producers_list[producer], 2)

    def test_place_order(self):
        """
        Tests if place order returns the expected products
        """
        first_product = Coffee("Brasil", 1, "5.09", "MEDIUM")
        second_product = Tea("Wild Cherry", 4, "Wild Cherry")
        producer = self.marketplace.register_producer()
        cart = self.marketplace.new_cart()

        self.marketplace.publish(producer, first_product)
        self.marketplace.publish(producer, second_product)

        self.marketplace.add_to_cart(cart, first_product)
        self.marketplace.add_to_cart(cart, second_product)

        ordered_products = self.marketplace.place_order(cart)

        self.assertEqual(ordered_products[0], first_product)
        self.assertEqual(ordered_products[1], second_product)
