from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', home_view, name='home'),
    path('courses/', include('courses.urls')),
    path('videos/', include('videos.urls')),  # 🆕 هذا هو السطر الجديد
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
