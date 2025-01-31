import csv
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Import data from a CSV file into a specified model."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path of the CSV file")
        parser.add_argument("model_name", type=str, help="Name of the model")

    def handle(self, *args, **options):

        file_path = options["file_path"]
        model_name = options["model_name"].capitalize()

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break  # Stop searching if the model is found
            except LookupError:
                continue  # Model not found in this app, continue searching

        if model is None:
            raise CommandError(f"Model '{model_name}' not found in any app.")

        model_fields = {field.name for field in model._meta.fields if not field.auto_created}
        unique_field = None

        for field in model._meta.fields:
            if field.unique and not field.primary_key:
                unique_field = field.name
                break
        if not unique_field:
            unique_field = model._meta.pk.name  

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                csv_headers = set(reader.fieldnames)

                missing_fields = model_fields - csv_headers
                extra_fields = csv_headers - model_fields

                if missing_fields:
                    raise CommandError(f"CSV file is missing required fields: {', '.join(missing_fields)}")
                
                if extra_fields:
                    self.stdout.write(
                        self.style.WARNING(f"Warning: CSV contains extra fields that will be ignored: {', '.join(extra_fields)}"))

                records_created = 0
                for row in reader:
                    try:
                        filtered_data = {key: value for key, value in row.items() if key in model_fields}
                        
                        if model.objects.filter(**{unique_field: filtered_data.get(unique_field)}).exists():
                            self.stdout.write(self.style.WARNING(f"{filtered_data.get(unique_field)} record already exists."))
                        else:
                            model.objects.create(**filtered_data)
                            records_created += 1

                    except IntegrityError as e:
                        self.stderr.write(self.style.ERROR(f"Error inserting row {row}: {e}"))

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully imported {records_created} new records into {model_name}.")
                )

        except FileNotFoundError:
            raise CommandError(f"File '{file_path}' not found.")
        except Exception as e:
            raise CommandError(f"An unexpected error occurred: {e}")
