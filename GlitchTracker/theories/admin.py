from django.contrib import admin
from .models import Theory
from proofs.models import Proof  


class ProofInline(admin.TabularInline):
    """Таблица доказательств, связанных с данной теорией."""
    model = Proof
    extra = 1
    fields = ['title', 'verified', 'evidence_link']


@admin.register(Theory)
class TheoryAdmin(admin.ModelAdmin):
    """Настройки админки для теории."""
    list_display = ['title', 'anomaly', 'votes', 'author', 'id']
    list_editable = ['votes']  
    list_filter = ['anomaly', 'votes', 'author']
    search_fields = ['title', 'explanation']
    raw_id_fields = ['anomaly', 'author'] 
    inlines = [ProofInline] 