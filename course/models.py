from django.db import models
from django.db import models
from tinymce.models import HTMLField

class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    content = HTMLField()

    def __str__(self):
        return self.title
