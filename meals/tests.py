from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase

from recipes.models import RecipeIngredient, Recipe
from .models import Meal, MealStatus


User = get_user_model()

   

class MealTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('cfe', password='abc123')
        self.user_id = self.user_a.id
        self.recipe_a = Recipe.objects.create(
            name='Grilled Chicken',
            user = self.user_a
        )
        self.recipe_b = Recipe.objects.create(
            name='Grilled Chicken Tacos',
            user = self.user_a
        )
        self.recipe_c = Recipe.objects.create(
            name='Nachos',
            user = self.user_a
        )
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Chicken',
            quantity='1/2',
            unit='pound'
        )
        self.recipe_ingredient_b = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Chicken',
            quantity='asdfasd',
            unit='pound'
        )
        self.meal = Meal.objects.create(
            user=self.user_a,
            recipe=self.recipe_a
        )
        meal_b = Meal.objects.create(
            user=self.user_a,
            recipe=self.recipe_a,
            status = MealStatus.COMPLETED
        )

    def test_pending_meals(self):
        qs = Meal.objects.all().pending()
        self.assertEqual(qs.count(), 1)
        qs1 = Meal.objects.by_user_id(self.user_id).pending()
        self.assertEqual(qs1.count(), 1)

    def test_completed_meals(self):
        qs = Meal.objects.all().completed()
        self.assertEqual(qs.count(), 1)
        qs1 = Meal.objects.by_user_id(self.user_id).completed()
        self.assertEqual(qs1.count(), 1)

    def test_add_item_via_toggle(self):
        meal_b = Meal.objects.create(
            user=self.user_a,
            recipe=self.recipe_a
        )
        qs1 = Meal.objects.by_user_id(self.user_id).pending()
        self.assertEqual(qs1.count(), 2)
        added = Meal.objects.toggle_in_queue(self.user_id, self.recipe_c.id)
        qs2 = Meal.objects.by_user_id(self.user_id).pending()
        self.assertEqual(qs2.count(), 3)   
        self.assertTrue(added)

    def test_remove_item_via_toggle(self):
        added = Meal.objects.toggle_in_queue(self.user_id, self.recipe_a.id)
        qs2 = Meal.objects.by_user_id(self.user_id).pending()
        self.assertEqual(qs2.count(), 0)   
        self.assertFalse(added)
    