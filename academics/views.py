from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department, Semester, Batch, Subject, ClassLog, Chapter, Topic, AcademicSession
from .forms import SubjectForm, AdminSubjectForm, FacultyForm, BatchForm, SessionForm
from django.contrib.auth.models import User, Group

# ==========================================
# 1. FACULTY FEATURES (Log & View)
# ==========================================

@login_required
def log_engagement(request):
    """
    Renders the main form where faculty enter data.
    """
    if request.method == "POST":
        try:
            # 1. Get Data
            subject_id = request.POST.get('subject')
            batch_id = request.POST.get('batch')
            chapter_id = request.POST.get('chapter')
            topic_name = request.POST.get('topic') # Text input
            date = request.POST.get('date')
            duration = request.POST.get('duration')

            subject = Subject.objects.get(id=subject_id)
            batch = Batch.objects.get(id=batch_id)

            # 2. Smart Topic Logic
            if chapter_id:
                chapter = Chapter.objects.get(id=chapter_id)
            else:
                chapter, _ = Chapter.objects.get_or_create(
                    subject=subject,
                    name="General Class Logs",
                    defaults={'added_by': request.user}
                )

            topic_id_or_name = request.POST.get('topic')
            if topic_id_or_name and str(topic_id_or_name).isdigit():
                 topic = Topic.objects.get(id=topic_id_or_name)
            else:
                topic, _ = Topic.objects.get_or_create(
                    chapter=chapter,
                    name=topic_id_or_name
                )

            # 3. Get Active Session
            active_session = AcademicSession.objects.filter(is_active=True).first()
            if not active_session:
                active_session = AcademicSession.objects.last()

            # 4. Save
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
    """ Shows the list of past logs for the logged-in teacher. """
    logs = ClassLog.objects.filter(faculty=request.user).select_related('subject', 'batch', 'topic').order_by('-date')
    return render(request, 'academics/history.html', {'logs': logs})

@login_required
def delete_log(request, log_id):
    """ Allows faculty to delete their own logs. """
    log = get_object_or_404(ClassLog, id=log_id, faculty=request.user)
    if request.method == "POST":
        log.delete()
        messages.success(request, "Log entry deleted.")
        return redirect('faculty_history')
    return render(request, 'academics/confirm_delete.html', {'object': log, 'type': 'Log Entry'})

@login_required
def faculty_dashboard(request):
    return render(request, 'users/dashboard.html')


# ==========================================
# 2. ADMIN PANEL FEATURES
# ==========================================

# --- A. Subject Manager ---
@login_required
def manage_subjects(request):
    is_admin = request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()
    if is_admin:
        subjects = Subject.objects.all().select_related('department', 'semester', 'faculty').order_by('department', 'code')
    else:
        subjects = Subject.objects.filter(faculty=request.user).select_related('department', 'semester').order_by('code')
    return render(request, 'academics/manage_subjects.html', {'subjects': subjects, 'is_admin': is_admin})

@login_required
def add_subject(request):
    is_admin = request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()
    FormClass = AdminSubjectForm if is_admin else SubjectForm
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            if is_admin: form.save()
            else:
                s = form.save(commit=False)
                s.faculty = request.user
                s.save()
            messages.success(request, "Subject created successfully!")
            return redirect('manage_subjects')
    else:
        form = FormClass()
    return render(request, 'academics/subject_form.html', {'form': form, 'title': 'Add New Subject'})

@login_required
def edit_subject(request, subject_id):
    is_admin = request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()
    if is_admin: subject = get_object_or_404(Subject, id=subject_id)
    else: subject = get_object_or_404(Subject, id=subject_id, faculty=request.user)
    
    FormClass = AdminSubjectForm if is_admin else SubjectForm
    if request.method == 'POST':
        form = FormClass(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated!")
            return redirect('manage_subjects')
    else:
        form = FormClass(instance=subject)
    return render(request, 'academics/subject_form.html', {'form': form, 'title': f'Edit {subject.code}'})

@login_required
def delete_subject(request, subject_id):
    is_admin = request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()
    if is_admin: subject = get_object_or_404(Subject, id=subject_id)
    else: subject = get_object_or_404(Subject, id=subject_id, faculty=request.user)
    
    if request.method == "POST":
        name = subject.name
        subject.delete()
        messages.success(request, f"Subject '{name}' deleted.")
        return redirect('manage_subjects')
    return render(request, 'academics/confirm_delete.html', {'object': subject, 'type': 'Subject'})


# --- B. Faculty Manager ---
@login_required
def manage_faculty(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()):
         return redirect('faculty_dashboard')
    try:
        faculty_group = Group.objects.get(name='Faculty')
        faculty_members = User.objects.filter(groups=faculty_group).order_by('first_name')
    except Group.DoesNotExist:
        faculty_members = []
    return render(request, 'academics/manage_faculty.html', {'faculty': faculty_members})

@login_required
def add_faculty(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()):
         return redirect('faculty_dashboard')
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, _ = Group.objects.get_or_create(name='Faculty')
            user.groups.add(group)
            messages.success(request, f"Faculty '{user.username}' created!")
            return redirect('manage_faculty')
    else:
        form = FacultyForm()
    return render(request, 'academics/faculty_form.html', {'form': form, 'title': 'Add New Faculty'})


# --- C. Batch Manager ---
@login_required
def manage_batches(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()):
         return redirect('faculty_dashboard')
    batches = Batch.objects.all().select_related('department', 'semester').order_by('department', 'name')
    return render(request, 'academics/manage_batches.html', {'batches': batches})

@login_required
def add_batch(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()):
         return redirect('faculty_dashboard')
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Batch created!")
            return redirect('manage_batches')
    else:
        form = BatchForm()
    return render(request, 'academics/form_template.html', {'form': form, 'title': 'Add New Batch'})


# --- D. Session Manager ---
@login_required
def manage_sessions(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()):
         return redirect('faculty_dashboard')
    sessions = AcademicSession.objects.all().order_by('-id')
    return render(request, 'academics/manage_sessions.html', {'sessions': sessions})

@login_required
def add_session(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()):
         return redirect('faculty_dashboard')
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            s = form.save()
            if s.is_active:
                AcademicSession.objects.exclude(id=s.id).update(is_active=False)
            messages.success(request, "Session created!")
            return redirect('manage_sessions')
    else:
        form = SessionForm()
    return render(request, 'academics/session_form.html', {'form': form, 'title': 'Start New Session'})

@login_required
def activate_session(request, session_id):
    if not (request.user.is_superuser or request.user.groups.filter(name='Faculty_Admin').exists()):
         return redirect('faculty_dashboard')
    session = get_object_or_404(AcademicSession, id=session_id)
    AcademicSession.objects.update(is_active=False)
    session.is_active = True
    session.save()
    messages.success(request, f"✅ Session '{session.name}' is now ACTIVE.")
    return redirect('manage_sessions')


# ==========================================
# 3. HTMX PARTIALS (Dropdown Logic)
# ==========================================

@login_required
def get_semesters(request):
    semesters = Semester.objects.all().order_by('name')
    return render(request, 'academics/partials/options_semester.html', {'options': semesters})

@login_required
def get_batches(request):
    dept_id = request.GET.get('department')
    sem_id = request.GET.get('semester')
    if not dept_id or not sem_id:
        return render(request, 'academics/partials/options_batch.html', {'options': []})
    batches = Batch.objects.filter(department_id=dept_id, semester_id=sem_id).order_by('name')
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














@login_required
def faculty_dashboard(request):
    # 1. Get User Groups
    user_groups = list(request.user.groups.values_list('name', flat=True))
    
    # 2. Get Recent Stats
    recent_stats = ClassLog.objects.filter(faculty=request.user) \
        .values('subject__name', 'batch__name', 'batch__semester__name') \
        .annotate(total_hours=Sum('duration_hours'), last_update=Max('created_at')) \
        .order_by('-last_update')[:4]
        
    # FIX: Get the Active Session to display on the dashboard
    current_session = AcademicSession.objects.filter(is_active=True).first()

    return render(request, 'users/dashboard.html', {
        'user_groups': user_groups,
        'recent_stats': recent_stats,
        'current_session': current_session  # <--- Sending this to HTML
    })



