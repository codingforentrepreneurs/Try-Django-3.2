from django.contrib.auth import get_user_model
from django.db.models import Sum

from meals.models import Meal
from recipes.models import RecipeIngredient

User = get_user_model()

def generate_meal_queue_totals(user):
    queue = Meal.objects.get_queue(user, prefetch_ingredients=True)
    ids = queue.values_list("recipe__recipeingredient__id", flat=True)
    qs = RecipeIngredient.objects.filter(id__in=ids)
    return qs.values("name", "unit").annotate(total=Sum("quantity_as_float"))