from django.db import models
from django.conf import settings
from students.models import Section  # تأكد من هذا السطر

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)  # 🆕 ربط الدرس بالقسم
    external_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class VideoProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    progress = models.FloatField(default=0)  # نسبة التقدم %
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')  # 🛡️ يمنع التكرار

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({self.progress}%)"
