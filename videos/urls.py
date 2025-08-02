from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ✅ لوحة التحكم (المعلم)
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/create/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:pk>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lessons/<int:pk>/delete/', views.lesson_delete, name='lesson_delete'),

    # ✅ عرض الدروس للطالب بحسب القسم
    path('lessons/student/', views.student_lesson_list, name='student_lesson_list'),

    # ✅ تحديث نسبة التقدم بالفيديو
    path('lessons/<int:lesson_id>/update_progress/', views.update_progress, name='update_progress'),
    # 🆕 صفحة الإحصائيات
    path('statistics/', views.lesson_statistics, name='lesson_statistics'),
    path('lessons/statistics/', views.lesson_statistics, name='lesson_statistics'),

]

# ✅ دعم رفع الفيديوهات
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
