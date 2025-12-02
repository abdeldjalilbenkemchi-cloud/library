from django.contrib import admin

# Register your models here.

from .models import Book 



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title', 'author', 'isbn', 'published_date', 'available', 'id')
    search_fields=('title', 'author', 'isbn')
    list_filter=('genre', 'available', 'published_date')
    list_display_links = ('title', 'isbn')
    list_editable=("available",)
    read_only_fields=('created_at', 'updated_at')
    date_hierarchy='published_date'
    ordering=('title',)

    fieldsets=(
        (None, {
            'fields': ('title', 'author', 'isbn', 'published_date', 'genre', 'available'),
            'classes':('collapse')
        }),

    )