from django.core.management.base import BaseCommand
from dataEntry.models import Student


class Command(BaseCommand):
    help = 'insert data to database'

    def handle(self, *args, **options):
        dataset = [
            {'roll_no': 1001, 'name': 'Karim', 'age': 25},
            {'roll_no': 1002, 'name': 'Tareq', 'age': 25},
            {'roll_no': 1003, 'name': 'Mortaza', 'age': 25},
            {'roll_no': 1004, 'name': 'Nawid', 'age': 24},
            {'roll_no': 1005, 'name': 'Monneb', 'age': 25},
        ]
        for data in dataset:
            
            roll = data['roll_no']
            name = data['name']
            age = data['age']

            recored_exist = Student.objects.filter(roll_no = roll).exists()
            if not recored_exist:
                Student.objects.create(roll_no=roll, name=name, age=age)
            else:
               self.stdout.write(self.style.WARNING(f' Student with roll number {roll} already exitst')) 
        return self.stdout.write(self.style.SUCCESS('Insert data succssfuly'))
