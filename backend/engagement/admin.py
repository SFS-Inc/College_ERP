from django.contrib import admin
from .models import ClassEngagement
from core.models import BatchSemester


@admin.register(ClassEngagement)
class ClassEngagementAdmin(admin.ModelAdmin):
    exclude = ('semester',)

    list_display = (
        'subject',
        'faculty',
        'batch',
        'semester',
        'date',
        'present_count',
        'total_students'
    )
    list_filter = ('batch', 'semester', 'subject')
    search_fields = ('chapter', 'topic')

    def save_model(self, request, obj, form, change):
        if not change:
            # Setting semester automatically from the active BatchSemester
            try:
                active_bs = BatchSemester.objects.get(
                    batch=obj.batch,
                    is_active=True
                )
                obj.semester = active_bs.semester
            except BatchSemester.DoesNotExist:
               raise ValidationError(
                    "No active semester found for the selected batch. "
                    "Please set an active semester before logging a class."
                )

        super().save_model(request, obj, form, change)
