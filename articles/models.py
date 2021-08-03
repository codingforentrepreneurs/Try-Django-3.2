from django.db import models
from django.db.models.signals import pre_save, post_save
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
        # if self.slug is None:
        #     self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # obj.save()
        # do another something


def article_pre_save(sender, instance, *args, **kwargs):
    print('pre_save')
    if instance.slug is None:
        instance.slug = slugify(instance.title)

pre_save.connect(article_pre_save, sender=Article)


def article_post_save(sender, instance, created, *args, **kwargs):
    print('post_save')
    if created:
        instance.slug = slugify(instance.title)
        instance.save()

post_save.connect(article_post_save, sender=Article)