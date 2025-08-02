from django.contrib import admin
from .models import Lesson
from students.models import Section  # ← ضروري لإظهار اسم القسم

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    admin.site.site_header = "لوحة التحكم للموقع التعليمي"
admin.site.site_title = "إدارة المحتوى"
admin.site.index_title = "مرحبا بك في لوحة الإدارة"
