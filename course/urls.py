from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChapterViewSet

router = DefaultRouter()
router.register(r'chapters', ChapterViewSet)

urlpatterns = [
    path('/api', include(router.urls)),
]
