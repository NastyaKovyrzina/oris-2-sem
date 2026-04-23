from django.contrib import admin
from .models import Anomaly, GlitchProfile
from theories.models import Theory  


class TheoryInline(admin.TabularInline):
    model = Theory
    extra = 1  
    fields = ['title', 'votes', 'author']  


@admin.register(Anomaly)
class AnomalyAdmin(admin.ModelAdmin):
    """Настройки админки для модели Аномалия."""
    list_display = ['title', 'location', 'danger_level', 'resolved', 'author', 'id']
    list_editable = ['danger_level', 'resolved'] 
    list_filter = ['danger_level', 'resolved', 'location']
    search_fields = ['title', 'description', 'location']
    raw_id_fields = ['author']  
    inlines = [TheoryInline]  


@admin.register(GlitchProfile)
class GlitchProfileAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'user', 'belief_level']
    list_editable = ['belief_level']
    list_filter = ['belief_level']
    search_fields = ['nickname', 'bio', 'user__username']  
    raw_id_fields = ['user']