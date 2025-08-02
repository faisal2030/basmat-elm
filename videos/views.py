from django.shortcuts import render, redirect, get_object_or_404
from .models import Lesson, VideoProgress
from .forms import LessonForm
from students.models import Student
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import models
# ✅ عرض دروس الطالب حسب قسمه
@login_required
def student_lesson_list(request):
    try:
        student = Student.objects.get(user=request.user)
        section = student.section
        lessons = Lesson.objects.filter(section=section).order_by('order')
    except Student.DoesNotExist:
        lessons = Lesson.objects.none()

    for lesson in lessons:
        vp = VideoProgress.objects.filter(user=request.user, lesson=lesson).first()
        lesson.progress = vp.progress if vp else 0

    return render(request, 'videos/student_lesson_list.html', {'lessons': lessons})


# ✅ عرض قائمة الدروس للإدارة
@login_required
def lesson_list(request):
    lessons = Lesson.objects.all().order_by('order')
    return render(request, 'videos/lesson_list.html', {'lessons': lessons})


# ✅ إضافة درس
@login_required
def lesson_create(request):
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lesson_list')
    else:
        form = LessonForm()
    return render(request, 'videos/lesson_form.html', {'form': form, 'form_title': '➕ إضافة درس'})


# ✅ تعديل درس
@login_required
def lesson_edit(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson_list')
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'videos/lesson_form.html', {'form': form, 'form_title': '✏️ تعديل الدرس'})


# ✅ حذف درس
@login_required
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        lesson.delete()
        return redirect('lesson_list')
    return render(request, 'videos/lesson_confirm_delete.html', {'lesson': lesson})


# ✅ تحديث نسبة مشاهدة الفيديو
@csrf_exempt
def update_progress(request, lesson_id):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            progress = data.get("progress", 0)

            lesson = Lesson.objects.get(id=lesson_id)
            vp, created = VideoProgress.objects.get_or_create(user=request.user, lesson=lesson)
            vp.progress = progress
            vp.save()

            return JsonResponse({"status": "success", "progress": progress})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
    # ✅ عرض إحصائيات المشاهدة
@login_required
def lesson_statistics(request):
    if request.user.is_staff:
        # 📌 للمعلم: عرض كل الدروس وإحصائيات الطلاب
        lessons = Lesson.objects.all().order_by('order')
        stats = []

        for lesson in lessons:
            progresses = VideoProgress.objects.filter(lesson=lesson)
            total_students = Student.objects.filter(section=lesson.section).count()
            viewers = progresses.count()
            avg_progress = progresses.aggregate(models.Avg('progress'))['progress__avg'] or 0

            stats.append({
                'lesson': lesson,
                'total_students': total_students,
                'viewers': viewers,
                'avg_progress': round(avg_progress, 2),
            })
    else:
        # 📌 للطالب: عرض تقدمه الشخصي فقط
        try:
            student = Student.objects.get(user=request.user)
            lessons = Lesson.objects.filter(section=student.section).order_by('order')
            stats = []

            for lesson in lessons:
                vp = VideoProgress.objects.filter(user=request.user, lesson=lesson).first()
                user_progress = vp.progress if vp else 0
                stats.append({
                    'lesson': lesson,
                    'user_progress': round(user_progress, 2),
                })
        except Student.DoesNotExist:
            stats = []

    return render(request, 'videos/statistics.html', {
        'stats': stats,
        'is_staff': request.user.is_staff,
    })
