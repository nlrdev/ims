import json
from decimal import Decimal
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.html import escape
from django.shortcuts import render
from bulk_update.helper import bulk_update
from store.models import Purchase, Material, Recipe, Ingredient
from store.forms import *



def forbidden():
    return HttpResponseForbidden()

def send_json(d):
    return HttpResponse(json.dumps(d), content_type="application/json")


def get_materials():
    qs = Material.objects.all()
    data = []
    for n in qs:
        if n.net_measure != 0:
            cpg = n.total_cost / n.net_measure
        else:
            cpg = 0
        data.append(
            {
                "name": n.name,
                "net_measure": str(n.net_measure),
                "total_cost": str(n.total_cost),
                "cost_per_gram": str(cpg),
            }
        )
    return HttpResponse(json.dumps(data), content_type="application/json")


def recalculate_materials():
    mqs = Material.objects.all()
    for m in mqs:
        m.total_cost = 0
        m.net_measure = 0
    bulk_update(mqs)
    pqs = Purchase.objects.select_related("type").all()
    for p in pqs:
        m = get_object_or_404(Material, pk=p.type.id)
        m.net_measure += Decimal(p.measure)
        m.total_cost += Decimal(p.price)
        m.save()
    data = []
    data.append({"status": "sorted"})
    return HttpResponse(json.dumps(data), content_type="application/json")


def add_material(request):
    data = []
    _name = escape(request.POST.get("name")).lower()
    if Material.objects.filter(name=_name).exists():
        data.append(
            {
                "status": "failed",
            }
        )
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        instance = Material(name=_name)
        instance.save()
        data.append({"id": instance.pk, "text": instance.name})
        return HttpResponse(json.dumps(data), content_type="application/json")


def get_puchaces():
    qs = Purchase.objects.select_related("type").all()
    data = []
    for n in qs:
        data.append(
            {
                "type": n.type.name,
                "measure": str(n.measure),
                "price": str(n.price),
                "notes": n.notes,
                "date_of_purchase": str(n.date_of_purchase),
                "id": n.pk,
            }
        )
    return HttpResponse(json.dumps(data), content_type="application/json")


def add_purchase(request):
    _type = escape(request.POST.get("type"))
    _price = escape(request.POST.get("price"))
    _measure = escape(request.POST.get("measure"))
    _notes = escape(request.POST.get("notes"))
    _created = escape(request.POST.get("created"))
    _date_of_purchase = escape(request.POST.get("date_of_purchase"))
    mat = get_object_or_404(Material, pk=_type)
    mat.net_measure += Decimal(_measure)
    mat.total_cost += Decimal(_price)
    mat.save()
    instance = Purchase(
        type=mat,
        price=_price,
        measure=_measure,
        notes=_notes,
        created=_created,
        date_of_purchase=_date_of_purchase,
    )
    instance.save()
    data = []
    data.append({"status": "saved"})
    return HttpResponse(json.dumps(data), content_type="application/json")


def add_purchase_note(request):
    p = get_object_or_404(Purchase, pk=escape(request.POST.get("id")))
    p.notes = escape(request.POST.get("note"))
    p.save()
    data = []
    data.append({"status": "saved"})
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_recipes():
    qs = Recipe.objects.all()
    data = []
    for n in qs:
        data.append({"id": n.pk, "name": n.name, "notes": n.notes})
    return HttpResponse(json.dumps(data), content_type="application/json")


def add_recipe(request):
    data = []
    _name = escape(request.POST.get("name"))
    if Recipe.objects.filter(name=_name).exists():
        data.append(
            {
                "status": "failed",
            }
        )
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        instance = Recipe(name=_name)
        instance.save()
        data.append({"status": "saved"})
        return HttpResponse(json.dumps(data), content_type="application/json")


def update_recipe(request):
    r = get_object_or_404(Recipe, pk=escape(request.POST.get("id")))
    r.name = escape(request.POST.get("name"))
    r.notes = escape(request.POST.get("notes"))
    r.save()
    data = []
    data.append(
        {
            "name": r.name, 
            "notes": r.notes,
        }
    )
    return HttpResponse(json.dumps(data), content_type="application/json")


def add_recipe_ingredient(request):
    recipe = get_object_or_404(Recipe, pk=escape(request.POST.get("id")))
    mat = get_object_or_404(Material, pk=escape(request.POST.get("type")))
    instance = Ingredient(type=mat, recipe=recipe, measure=escape(request.POST.get("qty")))
    instance.save()
    data = []
    data.append(
        {
            "id": instance.pk,
            "name": instance.type.name, 
            "qty": str(instance.measure),
        }
    )
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_recipe_ingredient(request):
    recipe = get_object_or_404(Recipe, pk=escape(request.POST.get("id")))
    ingredients = Ingredient.objects.filter(recipe=recipe)
    data = []
    for i in ingredients:
        data.append(
            {
                "id": i.pk,
                "name": i.type.name, 
                "qty": str(i.measure),
            }
        )
    return HttpResponse(json.dumps(data), content_type="application/json")

def delete_recipe_ingredient(request):
    Ingredient.objects.filter(pk=escape(request.POST.get("id"))).delete()
    data = []
    data.append({"status": "deleted"})
    return HttpResponse(json.dumps(data), content_type="application/json")