from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wanikani/', include('apps.wanikani.urls', namespace='wanikani')),
    path('', include('apps.blog.urls', namespace='posts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
