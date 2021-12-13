from store.api import *


def home(request):
    return render(request, "portal/home.html", {"page_script": "js/none.js"})


def material(request):
    if request.method == "GET":
        if is_ajax(request):
            return get_materials()
        else:
            return render(
                request, "portal/materials.html", {"page_script": "js/material.js"}
            )

    if is_post(request) and is_ajax(request):
        _type = escape(request.POST.get("request_type"))
        match _type:
            case "recalculate_materials":
                return recalculate_materials()
            case _:
                return forbidden()
                
    return forbidden()


def purchase(request):
    if request.method == "GET":
        if is_ajax(request):
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

    if is_post(request) and is_ajax(request):
        _type = escape(request.POST.get("request_type"))
        match _type:
            case "material_form":
                return add_material(request)
            case "note_form":
                return add_purchase_note(request)
            case "puchaces_form":
                return add_purchase(request)
            case _:
                return forbidden()

    return forbidden()


def recipe(request):
    if request.method == "GET":
        if is_ajax(request):
            return get_recipes()
        else:
            form = recipe_form()
            mats = Material.objects.all()
            selected_recipe = request.session.get("selected_recipe")
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

    if is_post(request) and is_ajax(request):
        _type = escape(request.POST.get("request_type"))
        match _type:
            case "recipe_form":
                return add_recipe(request)
            case "recipe_ingredients":
                request.session["selected_recipe"] = escape(request.POST.get("name"))
                return get_recipe_ingredient(request)
            case "recipe_ingredient_form":
                return add_recipe_ingredient(request)
            case "delete_recipe_ingredient":
                return delete_recipe_ingredient(request)
            case "recipe_update_form":
                return update_recipe(request)
            case "deselect":
                request.session["selected_recipe"] = "none"
                return HttpResponse(json.dumps({"status": "removed"}), content_type="application/json")
            case _:
                return forbidden()

    return forbidden()
