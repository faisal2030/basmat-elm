from django.shortcuts import render, redirect, get_object_or_404
from .models import Lesson
from .forms import LessonForm
from django.contrib.auth.decorators import login_required

@login_required
def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'courses/lesson_list.html', {'lessons': lessons})

@login_required
def lesson_create(request):
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)  # ← مهم أن يكون هنا request.FILES
        if form.is_valid():
            form.save()
            return redirect('lesson_list')
    else:
        form = LessonForm()
    return render(request, 'courses/lesson_form.html', {'form': form})

@login_required
def lesson_edit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)  # ← أضف request.FILES هنا أيضًا
        if form.is_valid():
            form.save()
            return redirect('lesson_list')
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/lesson_form.html', {'form': form, 'lesson': lesson})

@login_required
def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        lesson.delete()
        return redirect('lesson_list')
    return render(request, 'courses/lesson_confirm_delete.html', {'lesson': lesson})

@login_required
def student_lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'courses/student_lessons.html', {'lessons': lessons})
