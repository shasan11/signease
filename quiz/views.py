from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Chapter
from .serializers import ChapterDetailSerializer

class ChapterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chapter.objects.all().prefetch_related(
        'quizzes__questions__options'
    )
    serializer_class = ChapterDetailSerializer
    
    @action(detail=True, methods=['get'])
    def quizzes(self, request, pk=None):
        chapter = self.get_object()
        serializer = self.get_serializer(chapter)
        return Response(serializer.data)