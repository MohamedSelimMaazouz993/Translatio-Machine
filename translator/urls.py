from django.urls import path
from .views import translate
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('translate/', translate, name='translate'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
