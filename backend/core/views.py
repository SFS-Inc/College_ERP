from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subject, Batch
from engagement.models import ClassEngagement
from django.db.models import Q, Sum, Avg, F, ExpressionWrapper, FloatField
from datetime import datetime, date
from django.http import JsonResponse, HttpResponseForbidden
from core.models import BatchSemester

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def admin_dashboard(request):
    # Check for superuser or custom admin flag
    if not (request.user.is_superuser or getattr(request.user, "is_faculty_admin", False)):
        return HttpResponseForbidden("You are not allowed to access this page.")
    return render(request, 'admin_dashboard.html')

@login_required
def log_class(request):
    if request.method == "POST":
        batch_id = request.POST.get("batch")
        
        # 1. Resolve active semester for selected batch
        try:
            active_bs = BatchSemester.objects.get(
                batch_id=batch_id, 
                is_active=True
            )
        except BatchSemester.DoesNotExist:
            messages.error(request, "No active semester configured for the selected batch.")
            return redirect("log_class")

        # 2. Create ClassEngagement
        ClassEngagement.objects.create(
            faculty=request.user,
            batch=active_bs.batch,
            semester=active_bs.semester,
            subject_id=request.POST.get("subject"),
            chapter_id=request.POST.get("chapter"),
            topic=request.POST.get("topic"),
            date=request.POST.get("date"),
            hours_taken=request.POST.get("hours"),
            total_students=request.POST.get("total_students"),
            present_count=request.POST.get("present_count"),
            is_extra_class=request.POST.get("is_extra") == "on",
            notes=request.POST.get("notes")
        )
        messages.success(request, "Class logged successfully!")
        return redirect("dashboard")

    context = {
        "subjects": Subject.objects.all(),
        "batches": Batch.objects.all(),
        # No semesters needed in context; they are resolved automatically
    }
    return render(request, 'engagement/log_class.html', context)

@login_required
def get_active_semester(request):
    batch_id = request.GET.get('batch_id')
    if not batch_id:
        return JsonResponse({'error': 'No batch ID provided'}, status=400)
    
    try:
        bs = BatchSemester.objects.get(batch_id=batch_id, is_active=True)
        return JsonResponse({
            'semester_name': bs.semester.name,
            'semester_id': bs.semester.id
        })
    except BatchSemester.DoesNotExist:
        return JsonResponse({'error': 'No active semester found'}, status=404)

@login_required
def log_history(request):
    # Base query: Logs for the logged-in faculty
    logs = ClassEngagement.objects.filter(faculty=request.user).order_by('-date', '-created_at')

    # Filter by Subject
    subject_id = request.GET.get('subject')
    if subject_id:
        logs = logs.filter(subject_id=subject_id)

    # Filter by Batch
    batch_id = request.GET.get('batch')
    if batch_id:
        logs = logs.filter(batch_id=batch_id)

    # Filter by Date Range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        logs = logs.filter(date__gte=start_date)
    if end_date:
        logs = logs.filter(date__lte=end_date)

    # Filter by Extra Class
    extra = request.GET.get('extra')
    if extra == 'yes':
        logs = logs.filter(is_extra_class=True)
    elif extra == 'no':
        logs = logs.filter(is_extra_class=False)

    # Calculate Stats
    total_classes = logs.count()
    total_hours = logs.aggregate(total=Sum('hours_taken'))['total'] or 0
    
    avg_attendance = 0
    if total_classes > 0:
        agg_data = logs.aggregate(
            total_present=Sum('present_count'),
            total_students=Sum('total_students')
        )
        t_present = agg_data['total_present'] or 0
        t_students = agg_data['total_students'] or 0
        
        if t_students > 0:
            avg_attendance = round((t_present / t_students) * 100.0, 1)

    context = {
        'logs': logs,
        'subjects': Subject.objects.all(),
        'batches': Batch.objects.all(),
        'stats': {
            'total_classes': total_classes,
            'total_hours': total_hours,
            'avg_attendance': avg_attendance
        }
    }
    return render(request, 'engagement/log_history.html', context)

# --- Admin Modules ---

from django.contrib.auth import get_user_model

@login_required
def admin_faculty(request):
    if not (request.user.is_superuser or getattr(request.user, "is_faculty_admin", False)):
        return HttpResponseForbidden("Access Denied")
    
    User = get_user_model()
    # Fetch all faculty members (excluding students if any exist)
    faculty_members = User.objects.filter(role='STAFF').order_by('first_name', 'username')
    
    context = {
        'faculty_list': faculty_members
    }
    return render(request, 'custom_admin/admin_faculty.html', context)

@login_required
def admin_academics(request):
    if not (request.user.is_superuser or getattr(request.user, "is_faculty_admin", False)):
        return HttpResponseForbidden("Access Denied")
    return render(request, 'custom_admin/admin_academics.html')

@login_required
def admin_logs(request):
    if not (request.user.is_superuser or getattr(request.user, "is_faculty_admin", False)):
        return HttpResponseForbidden("Access Denied")
    # For now, redirecting to the existing log history, but clearly this could be a global log viewer later
    return redirect('log_history') 

@login_required
def admin_settings(request):
    if not (request.user.is_superuser or getattr(request.user, "is_faculty_admin", False)):
        return HttpResponseForbidden("Access Denied")
    return render(request, 'custom_admin/admin_settings.html')
