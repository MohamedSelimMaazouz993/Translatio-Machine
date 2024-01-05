from django.db import models

class Translation(models.Model):
    text = models.TextField()
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    translated_text = models.TextField()
    pdf_file = models.FileField(upload_to='pdf/', null=True, blank=True)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)
