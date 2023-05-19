from django.core.management import BaseCommand

from digital_agenda.apps.estat.importer import EstatDataset
from digital_agenda.common.console import console


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("code", help="ESTAT dataset code")

    def handle(self, *args, code, **options):
        dataset = EstatDataset(code)
        console.print("\nDataset loaded in the 'dataset' variable")
        import ipdb

        ipdb.set_trace()
        print(dataset)
