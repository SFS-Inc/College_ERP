from django.contrib import admin
from .models import Department, AcademicYear, AcademicSession, Semester, Batch, Subject, Chapter, Topic, ClassLog

# --- Smart Admin Views ---

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'semester')
    list_filter = ('department', 'semester')
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'faculty')
    list_filter = ('department', 'faculty')
    search_fields = ('name', 'code')

@admin.register(ClassLog)
class ClassLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'faculty', 'subject', 'batch', 'duration_hours', 'session')
    list_filter = ('session', 'date', 'faculty') # Filter by Session is crucial!

# --- Standard Registers ---
admin.site.register(Department)
admin.site.register(AcademicYear)
admin.site.register(AcademicSession) # <-- New!
admin.site.register(Semester)
admin.site.register(Chapter)
admin.site.register(Topic)