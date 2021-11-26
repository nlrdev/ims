from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=50)
    net_measure = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    total_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    cost_per_gram = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    UNITS = [
        ('G', 'g'),
        ('KG', 'kg'),
        ('ML', 'ml'),
        ('TSP', 'tsp'),
        ('TBP', 'tbp'),
        ]
    unit = models.CharField(
        max_length=3,
        choices=UNITS,
        default="G",
    )
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name



class Purchase(models.Model):
    type = models.ForeignKey(Material, related_name="mats", on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    measure = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    notes = models.TextField(default="")
    date_of_purchase = models.DateField(default="0000-00-00")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.type.name


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    notes = models.TextField(default="")
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    type = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
    measure = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    UNITS = [
    ('G', 'g'),
    ('KG', 'kg'),
    ('ML', 'ml'),
    ('TSP', 'tsp'),
    ('TBP', 'tbp'),
    ]
    unit = models.CharField(
        max_length=3,
        choices=UNITS,
        default="G",
    )

    def __str__(self):
        return self.type.name


class Products(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
    multiplier = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    created = models.DateTimeField(auto_now_add=True)


class Accessory(models.Model):
    name = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    notes = models.TextField(default="")

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    notes = models.TextField(default="")

    def __str__(self):
        return self.name


class Parts(models.Model):
    name = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    notes = models.TextField(default="")

    def __str__(self):
        return self.name


class Debit(models.Model):
    pass


class Credit(models.Model):
    pass
