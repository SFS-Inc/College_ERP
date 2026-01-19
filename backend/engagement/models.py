from django.db import models
from django.conf import settings
from core.models import Batch, Semester
from core.models import Subject, Chapter

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

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.CharField(max_length=200)

    date = models.DateField()
    # Replaced start_time with hours_taken
    hours_taken = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)

    total_students = models.PositiveIntegerField()
    present_count = models.PositiveIntegerField()
    
    # Added new fields
    is_extra_class = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} | {self.date} | {self.faculty}"
