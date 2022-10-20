from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from recipes.models import Recipe

from .signals import (meal_added, meal_removed)
"""
Meal 
- Pending
- Completed
- Expired
- Aborted

"""

User = settings.AUTH_USER_MODEL

class MealStatus(models.TextChoices):
    PENDING = 'p', 'Pending'
    COMPLETED = 'c', 'Completed'
    EXPIRED = 'e', 'Expired'
    ABORTED = 'a', 'Aborted'



class MealQuerySet(models.QuerySet):
    def by_user_id(self, user_id):
        return self.filter(user_id=user_id)
    
    def by_user(self, user):
        return self.filter(user=user)
    
    def pending(self):
        return self.filter(status=MealStatus.PENDING)

    def completed(self):
        return self.filter(status=MealStatus.COMPLETED)
        
    def aborted(self):
        return self.filter(status=MealStatus.ABORTED)
        
    def expired(self):
        return self.filter(status=MealStatus.EXPIRED)

    def in_queue(self, recipe_id):
        return self.pending().filter(recipe_id=recipe_id).exists()

   
class MealManager(models.Manager):
    def get_queryset(self):
        return MealQuerySet(self.model, using=self._db)

    def by_user_id(self, user_id):
        return self.get_queryset().by_user_id(user_id)
    
    def by_user(self, user):
        return self.get_queryset().by_user(user)

    def get_queue(self, user, prefetch_ingredients=False):
        qs = self.get_queryset().by_user(user).pending()
        if prefetch_ingredients:
            return qs.prefetch_related('recipe__recipeingredient')
        return qs

    def toggle_in_queue(self, user_id, recipe_id):
        qs = self.get_queryset().all().by_user_id(user_id)
        already_queued = qs.in_queue(recipe_id)
        added = None
        if already_queued:
            recipe_qs = qs.filter(recipe_id=recipe_id)
            for instance in recipe_qs:
                instance.status = MealStatus.ABORTED
                instance.save()
            added = False
        else:
            obj = self.model(
                user_id=user_id,
                recipe_id=recipe_id,
                status=MealStatus.PENDING
            )
            obj.save()
            added = True
        return added

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=1, choices=MealStatus.choices, default=MealStatus.PENDING)
    prev_status = models.CharField(max_length=1, null=True, choices=MealStatus.choices, default=None)

    objects = MealManager()



def meal_post_save(sender, instance, created, *args, **kwargs):
    if instance.status != instance.prev_status:
        if instance.status == MealStatus.PENDING:
            meal_added.send(sender=sender, instance=instance)
        if instance.status == MealStatus.ABORTED:
            meal_removed.send(sender=sender, instance=instance)
        instance.prev_status = instance.status
        instance.save()

post_save.connect(meal_post_save, sender=Meal)