from rest_framework import serializers
from .models import Theory
from anomalies.serializers import UserSerializer

class TheorySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Theory
        fields = ['id', 'title', 'explanation', 'votes', 'author', 'anomaly']