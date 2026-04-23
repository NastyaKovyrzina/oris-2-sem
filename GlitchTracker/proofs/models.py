from django.db import models
from theories.models import Theory

class Proof(models.Model):
    theory = models.ForeignKey(Theory, on_delete=models.CASCADE, verbose_name="Теория")

    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")

    evidence_link = models.URLField("Ссылка")
    verified = models.BooleanField("Подтверждено или нет", default=False)

    class Meta:
        verbose_name = "Доказательство"
        verbose_name_plural = "Доказательства"

    def __str__(self):
        return self.title