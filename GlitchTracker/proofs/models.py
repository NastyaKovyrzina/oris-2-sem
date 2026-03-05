from django.db import models
from theories.models import Theory

class Proof(models.Model):
    theory = models.ForeignKey(Theory, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()

    evidence_link = models.URLField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title