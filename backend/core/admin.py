from django.contrib import admin
from .models import Department
from .models import Subject
from .models import Batch, Semester

from .models import Semester, BatchSemester


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display=('name', 'created_at')
    search_fields=('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display=('code', 'name', 'department')
    list_filter=('department',)
    search_fields=('code', 'name')


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'joining_year', 'is_active')
    list_filter = ('course_name', 'is_active')
    search_fields = ('course_name',)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('number', 'name')
    ordering = ('number',)


@admin.register(BatchSemester)
class BatchSemesterAdmin(admin.ModelAdmin):
    list_display = ('batch', 'semester', 'is_active')
    list_filter = ('batch', 'is_active')

    def save_model(self, request, obj, form, change):
        # Ensure only one active semester per batch
        if obj.is_active:
            BatchSemester.objects.filter(
                batch=obj.batch
            ).exclude(pk=obj.pk).update(is_active=False)

        super().save_model(request, obj, form, change)