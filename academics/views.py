from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department, Semester, Batch, Subject, ClassLog, Chapter, Topic, AcademicSession
from .forms import SubjectForm  # Make sure forms.py exists!

# ==========================================
# 1. LOG ENGAGEMENT (The Main Feature)
# ==========================================

@login_required
def log_engagement(request):
    if request.method == "POST":
        try:
            # Get Data
            subject_id = request.POST.get('subject')
            batch_id = request.POST.get('batch')
            chapter_id = request.POST.get('chapter')
            topic_name = request.POST.get('topic') 
            date = request.POST.get('date')
            duration = request.POST.get('duration')

            subject = Subject.objects.get(id=subject_id)
            batch = Batch.objects.get(id=batch_id)

            # Smart Topic Logic
            if chapter_id:
                chapter = Chapter.objects.get(id=chapter_id)
            else:
                chapter, _ = Chapter.objects.get_or_create(
                    subject=subject,
                    name="General Class Logs",
                    defaults={'added_by': request.user}
                )

            topic, _ = Topic.objects.get_or_create(
                chapter=chapter,
                name=topic_name
            )

            # Active Session Logic
            active_session = AcademicSession.objects.filter(is_active=True).first()
            if not active_session:
                active_session = AcademicSession.objects.last()

            # Save
            ClassLog.objects.create(
                faculty=request.user,
                session=active_session,
                subject=subject,
                batch=batch,
                chapter=chapter,
                topic=topic,
                date=date if date else "2025-11-25",
                duration_hours=duration
            )
            
            messages.success(request, "✅ Class logged successfully!")
            return redirect('faculty_dashboard')

        except Exception as e:
            messages.error(request, f"Error saving log: {str(e)}")
    
    # GET Request
    departments = Department.objects.all()
    my_subjects = Subject.objects.filter(faculty=request.user).select_related('semester', 'department')

    return render(request, 'academics/log_form.html', {
        'departments': departments,
        'my_subjects': my_subjects
    })

@login_required
def faculty_history(request):
    logs = ClassLog.objects.filter(faculty=request.user).select_related('subject', 'batch', 'topic').order_by('-date')
    return render(request, 'academics/history.html', {'logs': logs})

@login_required
def faculty_dashboard(request):
    return render(request, 'users/dashboard.html')


# ==========================================
# 2. SUBJECT MANAGER (The Missing Part!)
# ==========================================

@login_required
def manage_subjects(request):
    """ List all subjects that belong to the logged-in faculty member. """
    my_subjects = Subject.objects.filter(faculty=request.user).select_related('department', 'semester')
    return render(request, 'academics/manage_subjects.html', {'subjects': my_subjects})

@login_required
def add_subject(request):
    """ Create a new subject. """
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.faculty = request.user
            subject.save()
            messages.success(request, f"Subject '{subject.name}' created successfully!")
            return redirect('manage_subjects')
    else:
        form = SubjectForm()
    
    return render(request, 'academics/subject_form.html', {'form': form, 'title': 'Add New Subject'})

@login_required
def edit_subject(request, subject_id):
    """ Edit an existing subject. """
    subject = get_object_or_404(Subject, id=subject_id, faculty=request.user)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully!")
            return redirect('manage_subjects')
    else:
        form = SubjectForm(instance=subject)
    
    return render(request, 'academics/subject_form.html', {'form': form, 'title': f'Edit {subject.code}'})


# ==========================================
# 3. HTMX PARTIALS (Dropdown Logic)
# ==========================================

@login_required
def get_semesters(request):
    semesters = Semester.objects.all().order_by('name')
    return render(request, 'academics/partials/options_semester.html', {'options': semesters})

@login_required
def get_batches(request):
    department_id = request.GET.get('department')
    semester_id = request.GET.get('semester')
    if not department_id or not semester_id:
        return render(request, 'academics/partials/options_batch.html', {'options': []})
    batches = Batch.objects.filter(department_id=department_id, semester_id=semester_id).order_by('name')
    return render(request, 'academics/partials/options_batch.html', {'options': batches})

@login_required
def get_chapters(request):
    subject_id = request.GET.get('subject')
    if not subject_id:
        return render(request, 'academics/partials/options_chapter.html', {'options': []})
    chapters = Chapter.objects.filter(subject_id=subject_id).order_by('name')
    return render(request, 'academics/partials/options_chapter.html', {'options': chapters})

@login_required
def get_topics(request):
    chapter_id = request.GET.get('chapter')
    if not chapter_id:
        return render(request, 'academics/partials/options_topic.html', {'options': []})
    topics = Topic.objects.filter(chapter_id=chapter_id).order_by('name')
    return render(request, 'academics/partials/options_topic.html', {'options': topics})