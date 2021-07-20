from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.TextField()
    content = models.TextField()