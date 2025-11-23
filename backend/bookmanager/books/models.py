from django.db import models
from locations.models import LocationRoot, Rack, Section


class Book(models.Model):
    title = models.CharField("Название", max_length=200)
    author = models.CharField("Автор", max_length=100)
    isbn = models.CharField("ISBN", max_length=13, unique=True, blank=True, null=True)
    total_copies = models.PositiveIntegerField("Всего экземпляров", default=1)
    available_copies = models.PositiveIntegerField("Доступно экземпляров", default=0)

    year = models.PositiveIntegerField("Год издания", null=True, blank=True)
    genre = models.CharField("Жанр", max_length=255, blank=True)
    description = models.TextField("Описание", blank=True)
    cover = models.URLField("Обложка", null=True, blank=True)
    pages = models.PositiveIntegerField("Количество страниц", null=True, blank=True)

    location_root = models.ForeignKey(LocationRoot, on_delete=models.SET_NULL, null=True)
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding and self.available_copies == 0:
            self.available_copies = self.total_copies

        if self.section and not self.rack:
            self.rack = self.section.rack

        if self.rack and not self.location_root:
            self.location_root = self.rack.location_root

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
