from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/create/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:lesson_id>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lessons/<int:lesson_id>/delete/', views.lesson_delete, name='lesson_delete'),
    
    # صفحة الدروس للطلاب
    path('lessons/student/', views.student_lesson_list, name='student_lesson_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
