from django.db import models
from django.conf import settings

# ==========================================
# 1. ORGANIZATION LAYER (Who are we?)
# ==========================================

class Department(models.Model):
    name = models.CharField(max_length=100) # e.g. "Computer Engineering"
    code = models.CharField(max_length=20, unique=True) # e.g. "CP08"
    current_semester = models.ForeignKey('Semester', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class AcademicYear(models.Model):
    # This is the Student's Level (e.g. "1st Year", "2nd Year")
    name = models.CharField(max_length=20) 

    def __str__(self):
        return self.name

class AcademicSession(models.Model):
    # This is the Calendar Time (e.g. "2025-2026")
    # The "Fresh Start" logic relies on this table.
    name = models.CharField(max_length=20, unique=True) 
    is_active = models.BooleanField(default=False) # Only ONE should be True at a time

    def __str__(self):
        status = " (Active)" if self.is_active else ""
        return f"{self.name}{status}"

class Semester(models.Model):
    # This is the Curriculum Time (e.g. "Semester 3")
    name = models.CharField(max_length=20) 
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.academic_year})"

class Batch(models.Model):
    name = models.CharField(max_length=10) # e.g. "A", "B"
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    class Meta:
        # Constraint: "CP15 Sem 3 Batch A" must be unique
        unique_together = ('department', 'semester', 'name')
        verbose_name_plural = "Batches"

    def __str__(self):
        # Shows as: "M2 - A" (Short and clean for dropdowns)
        return f"{self.department.code} {self.semester.name} - Batch {self.name}"

# ==========================================
# 2. CURRICULUM LAYER (What do we teach?)
# ==========================================

class Subject(models.Model):
    name = models.CharField(max_length=200) # e.g. "Meteorology"
    code = models.CharField(max_length=20, null=True, blank=True) # e.g. "MET101"
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    
    # SECURITY: Only THIS faculty member can see/log this subject
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.faculty.username})"

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=200) # e.g. "Atmospheric Dynamics"
    
    # AUDIT TRAIL: We track who added it, but we don't block it with 'is_approved' anymore
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    name = models.CharField(max_length=200) # e.g. "Pressure Systems"

    def __str__(self):
        return self.name

# ==========================================
# 3. LOGGING LAYER (The Work Diary)
# ==========================================

class ClassLog(models.Model):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # The "Time Bucket" - This allows us to reset the dashboard every year
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    
    date = models.DateField()
    duration_hours = models.DecimalField(max_digits=4, decimal_places=2) # e.g. 1.50
    
    # The Hierarchy of the Log
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.date}"



class ClassLog(models.Model):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    
    date = models.DateField()
    duration_hours = models.DecimalField(max_digits=4, decimal_places=2)
    
    # The Full Hierarchy
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    
    # NEW: Explicit links to Chapter and Topic
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.topic} ({self.date})"