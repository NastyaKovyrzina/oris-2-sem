from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
@receiver(post_save, sender=User)
def create_glitch_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        GlitchProfile.objects.get_or_create(
            user=instance,
            defaults={
                'nickname': instance.username,
                'belief_level': 50,
                'bio': ''
            }
        )
