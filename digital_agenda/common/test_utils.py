from django.test import TestCase
from rest_framework.test import APIClient


class APIBaseTest(TestCase):
    client_class = APIClient
    maxDiff = None
