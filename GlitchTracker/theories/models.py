from django.db import models
from anomalies.models import Anomaly
from django.contrib.auth.models import User

class Theory(models.Model):
    anomaly = models.ForeignKey(Anomaly, on_delete=models.CASCADE, verbose_name="Аномалия", related_name="theories")

    title = models.CharField("Название", max_length=200)
    explanation = models.TextField("Объяснение")

    votes = models.IntegerField("Голоса", default=0)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Автор", null=True, blank=True,)

    class Meta:
        verbose_name = "Теория"
        verbose_name_plural = "Теории"

    def __str__(self):
        return self.title