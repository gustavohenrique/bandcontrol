"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from rede.firewall import *

class SimpleTest(TestCase):
    def bloquear_ip_temporariamente(self):
        """
        Tests that 1 + 1 always equals 2.
        """

        self.assertEqual(1,1)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

