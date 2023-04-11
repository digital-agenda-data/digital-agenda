import datetime
from unittest.mock import patch

from django.core import mail
from django.test import TestCase
from pytz import UTC

from digital_agenda.apps.estat.jobs import check_all_configs_for_updates
from digital_agenda.apps.estat.jobs import check_estat_dataset_for_updates
from digital_agenda.apps.estat.jobs import send_estat_update_alerts
from digital_agenda.apps.estat.jobs import User
from digital_agenda.apps.estat.models import ImportConfig

THE_FUTURE = datetime.datetime(5542, 1, 1, tzinfo=UTC)


class TestCheckUpdates(TestCase):
    fixtures = ["geogroups", "test/importconfig.json"]

    def setUp(self):
        super().setUp()
        self.config = ImportConfig.objects.first()
        self.config.run_import(delete_existing=True, force_download=True)

    def test_no_update(self):
        check_estat_dataset_for_updates(self.config.code)

        self.config.refresh_from_db()
        self.assertEqual(self.config.new_version_available, False)

    def test_update_version(self):
        self.config.datastructure_last_version = "Monomon"
        self.config.save()

        check_estat_dataset_for_updates(self.config.code)

        self.config.refresh_from_db()
        self.assertEqual(self.config.new_version_available, True)

    def test_update_data_last_update(self):
        self.config.data_last_update = THE_FUTURE
        self.config.save()

        check_estat_dataset_for_updates(self.config.code)

        self.config.refresh_from_db()
        self.assertEqual(self.config.new_version_available, True)

    def test_update_datastructure_last_update(self):
        self.config.datastructure_last_update = THE_FUTURE
        self.config.save()

        check_estat_dataset_for_updates(self.config.code)

        self.config.refresh_from_db()
        self.assertEqual(self.config.new_version_available, True)


class TestSendAlert(TestCase):
    fixtures = ["geogroups", "test/importconfig.json"]

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            email="super@example.com", password="foo"
        )
        self.config = ImportConfig.objects.first()

    def test_no_send(self):
        send_estat_update_alerts()
        self.assertEqual(len(mail.outbox), 0)

    def test_send_alert(self):
        self.config.new_version_available = True
        self.config.save()

        send_estat_update_alerts()
        self.assertEqual(len(mail.outbox), 1)

        msg = mail.outbox[0]
        self.assertEqual(msg.to, [self.user.email])


class TestCheckAll(TestCase):
    fixtures = ["geogroups", "test/importconfig.json"]

    def setUp(self):
        super().setUp()
        self.config = ImportConfig.objects.first()
        self.mock = patch(
            "digital_agenda.apps.estat.jobs.check_estat_dataset_for_updates"
        ).start()

    def tearDown(self):
        patch.stopall()

    def test_check_code(self):
        self.config.datastructure_last_version = "Herrah"
        self.config.new_version_available = False
        self.config.save()

        check_all_configs_for_updates()
        self.mock.delay.assert_called_with(
            self.config.code, job_id="check_estat_dataset_for_updates(isoc_ci_cm_h)"
        )

    def test_ignore_no_last_version(self):
        self.config.datastructure_last_version = None
        self.config.new_version_available = False
        self.config.save()

        check_all_configs_for_updates()
        self.mock.delay.assert_not_called()

    def test_ignore_new_version_available(self):
        self.config.datastructure_last_version = "Lurien"
        self.config.new_version_available = True
        self.config.save()

        check_all_configs_for_updates()
        self.mock.delay.assert_not_called()
