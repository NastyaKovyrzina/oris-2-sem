from django.db import models
from anomalies.models import Anomaly
from django.contrib.auth.models import User

class Theory(models.Model):
    anomaly = models.ForeignKey(Anomaly, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    explanation = models.TextField()

    votes = models.IntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title