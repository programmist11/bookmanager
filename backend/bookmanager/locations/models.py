from django.db import models


class LocationRoot(models.Model):
    """
    Корневая сущность для любого объекта, где есть стеллажи/полки.
    Может быть:
    - библиотека
    - склад
    - архив
    - магазин
    - серверная комната
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Rack(models.Model):  # вместо Shelving
    root = models.ForeignKey(
        LocationRoot,
        on_delete=models.CASCADE,
        related_name="racks"
    )
    number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.root.name} — Рад {self.number}"


class Section(models.Model):  # вместо Shelf
    rack = models.ForeignKey(
        Rack,
        on_delete=models.CASCADE,
        related_name="sections"
    )
    number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.rack} — Секция {self.number}"


