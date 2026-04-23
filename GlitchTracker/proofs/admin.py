from django.contrib import admin
from .models import Proof


@admin.register(Proof)
class ProofAdmin(admin.ModelAdmin):
    list_display = ['title', 'theory', 'verified', 'evidence_link']
    list_editable = ['verified']
    list_filter = ['verified', 'theory']
    search_fields = ['title', 'description']
    raw_id_fields = ['theory']