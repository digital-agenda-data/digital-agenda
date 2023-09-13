from django.apps import AppConfig


class Config(AppConfig):
    name = "digital_agenda.apps.accounts"
    verbose_name = "Accounts"

    def ready(self):
        import digital_agenda.apps.accounts.jobs  # noqa
