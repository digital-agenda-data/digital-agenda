import shutil
from unittest.mock import patch
from unittest.mock import patch

from betamax.fixtures.unittest import BetamaxTestCase
from django.conf import settings
from django.conf import settings
from django.test import TestCase
from django.test import TestCase
from rest_framework.test import APIClient


class APIBaseTest(TestCase):
    client_class = APIClient
    maxDiff = None


class BetamaxPatchTestCase(BetamaxTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self._mock_session = patch(
            "requests.Session", return_value=self.session
        ).start()

    def tearDown(self):
        super().tearDown()
        patch.stopall()

        shutil.rmtree(settings.ESTAT_DOWNLOAD_DIR, ignore_errors=True)
        settings.ESTAT_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
