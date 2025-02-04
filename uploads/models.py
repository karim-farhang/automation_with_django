from django.db import models

# Create your models here.
class Upload(models.Model):
    csv_file = models.FileField(upload_to='uplodes/')
    model_name = models.CharField(max_length=200)
    uploded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model_name
