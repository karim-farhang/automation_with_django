from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'greeting commmand'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='spicific user name')

    def handle(self, *args, **options):
        name = options['name']
        greeting = f'Hi {name}, Good morining'
        return self.stdout.write(greeting)
