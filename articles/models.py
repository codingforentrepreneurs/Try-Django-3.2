from django.db import models
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.
class Article(models.Model):
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#model-field-types
    # Django model-field-types
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # obj = Article.objects.get(id=1)
        # set something
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # obj.save()
        # do another something