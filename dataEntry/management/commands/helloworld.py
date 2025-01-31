from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Hello world commad'
    def handle(self, *args, **options):
        self.stdout.write("Hello World")