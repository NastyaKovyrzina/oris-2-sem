from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Anomaly, GlitchProfile
from theories.models import Theory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GlitchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlitchProfile
        fields = ['nickname', 'belief_level', 'bio']

class TheorySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Theory
        fields = ['id', 'title', 'explanation', 'votes', 'author']

class AnomalySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    theories = TheorySerializer(many=True, read_only=True)

    class Meta:
        model = Anomaly
        fields = ['id', 'title', 'description', 'location', 'danger_level', 'resolved', 'author', 'theories']