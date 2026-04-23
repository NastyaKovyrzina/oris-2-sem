from django.db import models
from django.contrib.auth.models import User

class GlitchProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Профиль", related_name='glitch_profile')
    nickname = models.CharField("Никнейм", max_length=100)
    belief_level = models.IntegerField("Уровень веры в матрицу", default=50)
    bio = models.TextField("Био", blank=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.nickname