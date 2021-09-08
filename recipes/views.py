from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory # model form for querysets
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientImageForm
from .models import Recipe, RecipeIngredient
from .services import extract_text_via_ocr_service
# CRUD -> Create Retrieve Update & Delete

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "object_list": qs
    }
    return render(request, "recipes/list.html", context)


@login_required
def recipe_detail_view(request, id=None):
    hx_url = reverse("recipes:hx-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "recipes/detail.html", context) 


@login_required
def recipe_delete_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404
    if request.method == "POST":
        obj.delete()
        success_url = reverse('recipes:list')
        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "recipes/delete.html", context)


@login_required
def recipe_incredient_delete_view(request, parent_id=None, id=None):
    try:
        obj = RecipeIngredient.objects.get(recipe__id=parent_id, id=id, recipe__user=request.user)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404
    if request.method == "POST":
        name = obj.name
        obj.delete()
        success_url = reverse('recipes:detail', kwargs={"id": parent_id})
        if request.htmx:
            return render(request, "recipes/partials/ingredient-inline-delete-response.html", {"name": name})
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "recipes/delete.html", context)



@login_required
def recipe_detail_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is  None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "recipes/partials/detail.html", context) 


@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse("Created", headers=headers)
            # context = {
            #     "object": obj
            # }
            # return render(request, "recipes/partials/detail.html", context)
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context)  

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    new_ingredient_url = reverse("recipes:hx-ingredient-create", kwargs={"parent_id": obj.id})
    context = {
        "form": form,
        "object": obj,
        "new_ingredient_url": new_ingredient_url
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data saved.'
    if request.htmx:
        return render(request, "recipes/partials/forms.html", context)
    return render(request, "recipes/create-update.html", context)  


@login_required
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")
    instance = None
    if id is not None:
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj, id=id)
        except:
            instance = None
    form = RecipeIngredientForm(request.POST or None, instance=instance)
    url = reverse("recipes:hx-ingredient-create", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": instance
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "recipes/partials/ingredient-inline.html", context) 
    return render(request, "recipes/partials/ingredient-form.html", context) 



def recipe_ingredient_image_upload_view(request, parent_id=None):
    template_name = "recipes/upload-image.html"
    if request.htmx:
        template_name = "recipes/partials/image-upload-form.html"
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        raise Http404
    form = RecipeIngredientImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.recipe = parent_obj
        # obj.recipe_id = parent_id
        obj.save()
        # send image file -> microservice api
        # microservice api -> data about the file
        # cloud providers $$
        result = extract_text_via_ocr_service(obj.image)
        obj.extracted = result
        obj.save()
        # print(obj.extracted)

    return render(request, template_name, {"form":form})