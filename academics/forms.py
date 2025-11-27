from django import forms
from django.contrib.auth import get_user_model
from .models import Subject, Batch, AcademicSession

User = get_user_model()

# --- 1. Subject Forms ---

class SubjectForm(forms.ModelForm):
    """ Form for Regular Teachers (Auto-assigned faculty) """
    class Meta:
        model = Subject
        fields = ['name', 'code', 'department', 'semester']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Advanced Python'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. PY404'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
        }

class AdminSubjectForm(forms.ModelForm):
    """ Form for Admins (Can assign faculty manually) """
    class Meta:
        model = Subject
        fields = ['name', 'code', 'department', 'semester', 'faculty']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'faculty': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter dropdown to show only Faculty users
        self.fields['faculty'].queryset = User.objects.filter(groups__name='Faculty')
        self.fields['faculty'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name} ({obj.username})"


# --- 2. Faculty Management Form ---

class FacultyForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. John'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Doe'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. jdoe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. john@college.edu'}),
        }

    def save(self, commit=True):
        # Custom save method to Hash the password securely
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user 


# --- 3. Batch Management Form ---

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'department', 'semester']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
        }


# --- 4. Session Management Form ---

class SessionForm(forms.ModelForm):
    class Meta:
        model = AcademicSession
        fields = ['name', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. June 2024'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }