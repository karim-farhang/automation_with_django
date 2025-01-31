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

        # Find the model dynamically
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break  # Stop searching if the model is found
            except LookupError:
                continue  # Continue searching in other apps

        if model is None:
            raise CommandError(f"Model '{model_name}' not found in any app.")

        # Get model fields
        model_fields = {field.name for field in model._meta.fields if not field.auto_created}
        unique_field = None

        # Find a unique field (if available)
        for field in model._meta.fields:
            if field.unique and not field.primary_key:
                unique_field = field.name
                break
        if not unique_field:
            unique_field = model._meta.pk.name  # Default to primary key if no unique field exists

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                csv_headers = set(reader.fieldnames)

                # Ignore 'id' column if it exists in the CSV
                if "id" in csv_headers:
                    csv_headers.remove("id")

                # Validate required fields
                missing_fields = model_fields - csv_headers
                if missing_fields:
                    raise CommandError(f"CSV file is missing required fields: {', '.join(missing_fields)}")
                
                extra_fields = csv_headers - model_fields
                if extra_fields:
                    self.stdout.write(
                        self.style.WARNING(f"Warning: CSV contains extra fields that will be ignored: {', '.join(extra_fields)}")
                    )

                records_created = 0
                duplicates_found = 0

                for row in reader:
                    try:
                        # Remove fields not in the model and ignore empty values
                        filtered_data = {key: value for key, value in row.items() if key in model_fields and value.strip()}

                        # Check if a record with the same unique field already exists
                        if model.objects.filter(**filtered_data).exists():
                            duplicates_found += 1
                        else:
                            model.objects.create(**filtered_data)
                            records_created += 1

                    except IntegrityError as e:
                        self.stderr.write(self.style.ERROR(f"Error inserting row {row}: {e}"))

                self.stdout.write(self.style.SUCCESS(f"Successfully imported {records_created} new records into {model_name}."))
                if duplicates_found:
                    self.stdout.write(self.style.WARNING(f"Skipped {duplicates_found} duplicate records."))

        except FileNotFoundError:
            raise CommandError(f"File '{file_path}' not found.")
        except Exception as e:
            raise CommandError(f"An unexpected error occurred: {e}")
