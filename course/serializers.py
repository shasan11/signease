from rest_framework import serializers
from .models import Chapter

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'title', 'description', 'thumbnail', 'content']
