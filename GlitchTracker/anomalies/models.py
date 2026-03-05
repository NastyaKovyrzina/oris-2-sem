from django.db import models
from django.contrib.auth.models import User

class Anomaly(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)

    danger_level = models.CharField(max_length=50)
    resolved = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class GlitchProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(max_length=100)
    belief_level = models.IntegerField(default=50)
    bio = models.TextField()

    def __str__(self):
        return self.nickname