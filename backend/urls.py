from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin', admin.site.urls),
    path('quiz-api',include("quiz.urls")),
    path('course-api',include("course.urls")),
    path('auth/',include("djoser.urls")),
    path('auth/',include("djoser.urls.jwt")),
    path('tinymce/', include('tinymce.urls')),  # required for the widget
]
