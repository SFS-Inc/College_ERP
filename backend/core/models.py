from django.conf import settings
from django.db import models



class Department(models.Model):
    """

    This area represents deapartment like Computer Engineering or Mechatronics.

    """
    name=models.CharField(max_length=100, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    """
    This model represent subject taught under a department such as DSA,IoT,WSA.

    """
    code=models.CharField(max_length=20, unique=True)
    name=models.CharField(max_length=100)
    department=models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='subjects'
    )

    def __str__(self):
        return self.name


class Batch(models.Model):
    """
    Represents academic batches (e.g., 2024-2028).
    """
    course_name = models.CharField(max_length=50)
    joining_year = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course_name} ({self.joining_year})"


class Semester(models.Model):
    """
    Global semester definition.
    Example: Semester 1, Semester 2, etc.
    """

    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
        

class BatchSemester(models.Model):
    """
    Links a batch to a semester and defines
    which semester is currently active for the batch.
    """

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('batch', 'semester')

    def __str__(self):
        status = "ACTIVE" if self.is_active else "INACTIVE"
        return f"{self.batch} → {self.semester} ({status})"




