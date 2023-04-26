"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock
import logging
import logging.handlers
import time



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

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        file_handler = logging.handlers.RotatingFileHandler("marketplace.log", backupCount=10)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        formatter.converter = time.gmtime
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.logger.info("New producer: %s", self.producer_index)
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

        self.logger.info("Publishing product %s from producer %s", str(product), producer_id)

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
        self.logger.info("Registering new cart")

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
        self.logger.info("Adding product %s to cart %d", product, cart_id)

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
        self.logger.info("Remove product %s from cart %d", product, cart_id)

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
        self.logger.info("Place order from cart %d", cart_id)

        my_list = []
        for elem in self.carts_list[cart_id]:
            my_list.append(elem["product"])

        return my_list


