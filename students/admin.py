from django.contrib import admin
from .models import Student, Section

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'section']
    list_filter = ['section']
    search_fields = ['user__username', 'user__email']
