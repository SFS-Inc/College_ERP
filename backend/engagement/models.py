from django.db import models
from django.conf import settings
from core.models import Batch, Semester
from core.models import Subject
from core.models import Batch, Semester



class ClassEngagement(models.Model):
    """
    Logs a single class session conducted by a faculty.
    """

    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    chapter = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)

    date = models.DateField()
    start_time = models.TimeField()

    total_students = models.PositiveIntegerField()
    present_count = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} | {self.date} | {self.faculty}"
