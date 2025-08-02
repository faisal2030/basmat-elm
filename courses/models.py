from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)  # ← رفع الفيديو
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)  # ← تأكد من وجود هذا الحقل إن كنت تستخدمه في ordering

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
