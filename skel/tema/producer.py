"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

import time
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.products, self.marketplace, self.republish_wait_time, \
            self.product_no, self.producer_id = products, marketplace, republish_wait_time, 0, \
            marketplace.register_producer()

    def publish_product(self, product, quantity, wait_time, id_producer):
        iterator = 0
        # Publish a product in the given quantity
        while iterator < quantity:
            wait_publish = self.marketplace.publish(id_producer, product)
            # Producer must wait until the marketplace becomes available
            if wait_publish:
                iterator = iterator + 1
                time.sleep(wait_time)
            else:
                time.sleep(self.republish_wait_time)

    def run(self):
        while True:
            # Register the producer, generate id

            for prod in self.products:
                [product, quantity, wait_time] = [prod[0], prod[1], prod[2]]
                self.publish_product(product, quantity, wait_time, self.producer_id)
