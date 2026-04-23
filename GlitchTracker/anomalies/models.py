from django.db import models
from django.contrib.auth.models import User

class Anomaly(models.Model):
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    location = models.CharField("Локация", max_length=200)

    danger_level = models.CharField("Уровень опасности", max_length=50)
    resolved = models.BooleanField("Решено или нет", default=False)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Автор", null=True, blank=True,)

    image_path = models.CharField(
        'Путь к картинке',
        max_length=255,
        blank=True,
        help_text='Например: "img/anomalies/glitch.jpg"'
    )

    class Meta:
        verbose_name = "Аномалия"
        verbose_name_plural = "Аномалии"

    def __str__(self):
        return f"Аномалия: {self.title}"
        
class GlitchProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Профиль")

    nickname = models.CharField("Никнейм", max_length=100)
    belief_level = models.IntegerField("Уровень", default=50)
    bio = models.TextField("Био")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.nickname