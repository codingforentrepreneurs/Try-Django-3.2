from django.urls import path

from .views import (
    recipe_list_view,
    recipe_detail_view,
    recipe_delete_view,
    recipe_create_view,
    recipe_update_view,
    recipe_detail_hx_view,
    recipe_ingredient_update_hx_view,
    recipe_incredient_delete_view


)

app_name='recipes'

urlpatterns = [
    path("", recipe_list_view, name='list'),
    path("create/", recipe_create_view, name='create'),
    
    path("hx/<int:parent_id>/ingredient/<int:id>/", recipe_ingredient_update_hx_view, name='hx-ingredient-detail'),
    path("hx/<int:parent_id>/ingredient/", recipe_ingredient_update_hx_view, name='hx-ingredient-create'),
    path("hx/<int:id>/", recipe_detail_hx_view, name='hx-detail'),
    
    path("<int:parent_id>/ingredient/<int:id>/delete/", recipe_incredient_delete_view, name='ingredient-delete'),
    path("<int:id>/delete/", recipe_delete_view, name='delete'),
    path("<int:id>/edit/", recipe_update_view, name='update'),
    path("<int:id>/", recipe_detail_view, name='detail'),
]