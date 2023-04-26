"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock
import unittest
from product import Product, Coffee, Tea


class TestMarketPlace(unittest.TestCase):

    def setUp(self):
        """
        Sets up a mock marketplace with a queue of size 10 for producers
        """
        self.marketplace = Marketplace(10)

    def test_register_producer(self):
        """
        Tests if the registered producers get the correct ids
        """
        self.assertEqual(self.marketplace.register_producer(), 0)
        self.assertEqual(self.marketplace.register_producer(), 1)
        self.assertEqual(self.marketplace.register_producer(), 2)

    def test_publish(self):

        producer = self.marketplace.register_producer()
        first_product = Coffee("Brasil", 1, "5.09", "MEDIUM")
        second_product = Tea("Wild Cherry", 4, "Wild Cherry")

        """
        Tests if multiple products are correctly published to marketplace
        and the number of products/ producer is increased
        """
        self.marketplace.publish(producer, first_product)
        self.assertEqual(self.marketplace.producers_list[producer], 1)
        self.assertIn({'id': producer, 'product': first_product}, self.marketplace.products_list)
        self.marketplace.publish(producer, second_product)
        self.assertEqual(self.marketplace.producers_list[producer], 2)
        self.assertIn({'id': producer, 'product': second_product}, self.marketplace.products_list)

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
        first_product = Coffee("Brasil", 1, "5.09", "MEDIUM")
        second_product = Tea("Wild Cherry", 4, "Wild Cherry")
        producer = self.marketplace.register_producer()
        cart = self.marketplace.new_cart()

        self.marketplace.publish(producer, first_product)
        self.marketplace.publish(producer, second_product)

        self.marketplace.add_to_cart(cart, first_product)

        self.assertNotIn({'id': producer, 'product': first_product}, self.marketplace.products_list)
        self.assertEqual(self.marketplace.producers_list[producer], 1)
        self.assertIn({'id': producer, 'product': first_product}, self.marketplace.carts_list[cart])

        self.marketplace.add_to_cart(cart, second_product)

        self.assertNotIn({'id': producer, 'product': second_product}, self.marketplace.products_list)
        self.assertEqual(self.marketplace.producers_list[producer], 0)
        self.assertIn({'id': producer, 'product': second_product}, self.marketplace.carts_list[cart])

    def test_remove_from_cart(self):
        """
        Tests if the products are added to the cart correctly
        """
        first_product = Coffee("Brasil", 1, "5.09", "MEDIUM")
        second_product = Tea("Wild Cherry", 4, "Wild Cherry")
        producer = self.marketplace.register_producer()
        cart = self.marketplace.new_cart()

        self.marketplace.publish(producer, first_product)
        self.marketplace.publish(producer, second_product)

        self.marketplace.add_to_cart(cart, first_product)
        self.marketplace.add_to_cart(cart, second_product)

        self.marketplace.remove_from_cart(cart, first_product)
        self.assertIn({'id': producer, 'product': first_product}, self.marketplace.products_list)
        self.assertNotIn({'id': producer, 'product': first_product}, self.marketplace.carts_list[cart])
        self.assertEqual(self.marketplace.producers_list[producer], 1)

        self.marketplace.remove_from_cart(cart, second_product)
        self.assertIn({'id': producer, 'product': second_product}, self.marketplace.products_list)
        self.assertNotIn({'id': producer, 'product': second_product}, self.marketplace.carts_list[cart])
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


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor



        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        [self.producer_lock, self.cart_lock, self.products_lock] = [Lock(), Lock(), Lock()]
        self.queue_size_per_producer = queue_size_per_producer
        [self.producer_index, self.cart_index, self.products_list, self.producers_list, self.carts_list] = \
            [-1, -1, [], [], []]

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.producer_lock:
            self.producer_index += 1
            self.producers_list.append(0)
        return self.producer_index

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        producer_number_of_products = self.producers_list[producer_id]

        if producer_number_of_products < self.queue_size_per_producer:
            with self.products_lock:
                self.products_list.append({"id": producer_id, "product": product})
            with self.producer_lock:
                self.producers_list[producer_id] += 1
            return True
        else:
            return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.cart_lock:
            self.cart_index += 1
            self.carts_list.append([])
        return self.cart_index

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        my_list = list(filter(lambda products_element: products_element['product'] is product, self.products_list))
        if my_list:
            with self.cart_lock:
                self.carts_list[cart_id].append(my_list[0])
            with self.producer_lock:
                self.producers_list[my_list[0]["id"]] -= 1
            with self.products_lock:
                self.products_list.remove(my_list[0])
            return True
        else:
            return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        my_product = [element for element in self.carts_list[cart_id] if element["product"] is product][0]
        if my_product is not None:
            with self.producer_lock:
                self.producers_list[my_product["id"]] += 1
            with self.products_lock:
                self.products_list.append(my_product)
            with self.cart_lock:
                self.carts_list[cart_id].remove(my_product)
            return

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        my_list = []
        for elem in self.carts_list[cart_id]:
            my_list.append(elem["product"])

        return my_list
