from django.db import models
from django.conf import settings
from students.models import Section
from cloudinary.models import CloudinaryField  # ✅ مهم

class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان الدرس")
    description = models.TextField(verbose_name="وصف الدرس")

    # ✅ رفع الفيديو إلى Cloudinary كـ Video
    video_file = CloudinaryField(
        resource_type='video',
        folder='videos',
        blank=True,
        null=True,
        verbose_name="ملف الفيديو"
    )

    external_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="رابط خارجي (مثل YouTube أو Google Drive)"
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        verbose_name="القسم"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    order = models.IntegerField(default=0, verbose_name="ترتيب العرض")

    class Meta:
        ordering = ['order']
        verbose_name = "درس"
        verbose_name_plural = "الدروس"

    def __str__(self):
        return self.title


class VideoProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="المستخدم"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="الدرس"
    )
    progress = models.FloatField(default=0, verbose_name="نسبة التقدم (%)")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = "تقدم الفيديو"
        verbose_name_plural = "تقدم الفيديوهات"

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({self.progress}%)"
