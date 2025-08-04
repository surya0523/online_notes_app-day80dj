# notes/admin.py

from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('created_at', 'updated_at', 'user')
    readonly_fields = ('created_at', 'updated_at')