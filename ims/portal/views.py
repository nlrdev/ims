from store.api import *


def home(request):
    return render(request, "portal/home.html", {"page_script": "js/none.js"})


def material(request):
    if request.method == "GET":
        if request.is_ajax():
            return get_materials()
        else:
            return render(
                request, "portal/materials.html", {"page_script": "js/material.js"}
            )

    if request.method == "POST" and request.is_ajax():
        _type = escape(request.POST.get("request_type"))
        if _type == "recalculate_materials":
            return recalculate_materials()

    return forbidden()


def purchase(request):
    if request.method == "GET":
        if request.is_ajax():
            return get_puchaces()
        else:
            return render(
                request,
                "portal/purchases.html",
                {
                    "purchase_form": add_purchase_form(),
                    "material_form": add_material_form(),
                    "page_script": "js/purchase.js",
                },
            )

    if request.method == "POST" and request.is_ajax():
        _type = escape(request.POST.get("request_type"))
        if _type == "material_form":
            return add_material(request)
        if _type == "note_form":
            return add_purchase_note(request)
        if _type == "puchaces_form":
            return add_purchase(request)

    return forbidden()


def recipe(request):
    if request.method == "GET":
        if request.is_ajax():
            return get_recipes()
        else:
            form = recipe_form()
            mats = Material.objects.all()
            selected_recipe = request.session["selected_recipe"]
            return render(
                request,
                "portal/recipes.html",
                {
                    "form": form,
                    "mats": mats,
                    "page_script": "js/recipe.js",
                    "selected_recipe": selected_recipe,
                },
            )

    if request.method == "POST" and request.is_ajax():
        _type = escape(request.POST.get("request_type"))
        if _type == "recipe_form":
            return add_recipe(request)
        if _type == "recipe_ingredients":
            request.session["selected_recipe"] = escape(request.POST.get("name"))
            return get_recipe_ingredient(request)
        if _type == "recipe_ingredient_form":
            return add_recipe_ingredient(request)
        if _type == "delete_recipe_ingredient":
            return delete_recipe_ingredient(request)
        if _type == "recipe_update_form":
            return update_recipe(request)
        if _type == "deselect":
            request.session["selected_recipe"] = "none"
            data = []
            data.append({"status": "removed"})
            return HttpResponse(json.dumps(data), content_type="application/json")

    return forbidden()
