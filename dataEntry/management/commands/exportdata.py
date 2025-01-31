import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = "Export data from all tables in all apps into separate CSV files inside the 'data' directory."

    def handle(self, *args, **options):
        # Create data directory if it doesn't exist
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                model_name = model.__name__.lower()
                
                file_path = os.path.join(data_dir, f"{model_name}_data.csv")

                records = model.objects.all()
                if not records.exists():
                    self.stdout.write(self.style.WARNING(f"Skipping {model_name}: No records found."))
                    continue

                with open(file_path, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    fields = [field.name for field in model._meta.fields]
                    writer.writerow(fields)  # Write headers

                    for record in records:
                        writer.writerow([getattr(record, field) for field in fields])

                self.stdout.write(self.style.SUCCESS(f"Exported {model.objects.count()} records from '{model_name}' to {file_path}."))

        self.stdout.write(self.style.SUCCESS("Export process completed!"))
