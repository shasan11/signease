from django.contrib import admin
from .models import Chapter

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'thumbnail')
    search_fields = ('title',)

admin.site.register(Chapter, ChapterAdmin)
