from django.core.management.base import BaseCommand
from academics.models import Department, AcademicYear, Semester, Batch, AcademicSession

class Command(BaseCommand):
    help = 'Populates the database with Real College Structure (DICE/M series)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing College Data...")

        # 1. Academic Session (The "Time Bucket")
        session, _ = AcademicSession.objects.get_or_create(
            name="June 2024", 
            defaults={'is_active': True}
        )

        # 2. Departments
        dept_cp08, _ = Department.objects.get_or_create(name="Computer Engineering", code="CP08")
        dept_cp15, _ = Department.objects.get_or_create(name="Mechatronics", code="CP15")
        
        # 3. Student Levels
        year_1, _ = AcademicYear.objects.get_or_create(name="1st Year")
        year_2, _ = AcademicYear.objects.get_or_create(name="2nd Year")
        year_3, _ = AcademicYear.objects.get_or_create(name="3rd Year")

        # 4. Semesters
        # We create objects for Sem 1-6 and link them to years
        sem_1, _ = Semester.objects.get_or_create(name="Semester 1", academic_year=year_1)
        sem_2, _ = Semester.objects.get_or_create(name="Semester 2", academic_year=year_1)
        
        sem_3, _ = Semester.objects.get_or_create(name="Semester 3", academic_year=year_2)
        sem_4, _ = Semester.objects.get_or_create(name="Semester 4", academic_year=year_2)
        
        sem_5, _ = Semester.objects.get_or_create(name="Semester 5", academic_year=year_3)
        sem_6, _ = Semester.objects.get_or_create(name="Semester 6", academic_year=year_3)

        # 5. BATCHES (The Custom Naming Logic)

        # --- CP08 (DICE Series) ---
        # 1st Year -> DICE 1
        Batch.objects.get_or_create(name="DICE 1 - A", department=dept_cp08, semester=sem_1)
        Batch.objects.get_or_create(name="DICE 1 - A", department=dept_cp08, semester=sem_2)
        
        # 2nd Year -> DICE 2
        Batch.objects.get_or_create(name="DICE 2 - A", department=dept_cp08, semester=sem_3)
        Batch.objects.get_or_create(name="DICE 2 - A", department=dept_cp08, semester=sem_4)

        # 3rd Year -> DICE 3
        Batch.objects.get_or_create(name="DICE 3 - A", department=dept_cp08, semester=sem_5)
        Batch.objects.get_or_create(name="DICE 3 - A", department=dept_cp08, semester=sem_6)

        # --- CP15 (M Series) ---
        # They have multiple divisions (A, B, C, D)
        divisions = ['A', 'B', 'C', 'D']

        for div in divisions:
            # 1st Year -> M1
            Batch.objects.get_or_create(name=f"M1 - {div}", department=dept_cp15, semester=sem_1)
            Batch.objects.get_or_create(name=f"M1 - {div}", department=dept_cp15, semester=sem_2)

            # 2nd Year -> M2
            Batch.objects.get_or_create(name=f"M2 - {div}", department=dept_cp15, semester=sem_3)
            Batch.objects.get_or_create(name=f"M2 - {div}", department=dept_cp15, semester=sem_4)

            # 3rd Year -> M3
            Batch.objects.get_or_create(name=f"M3 - {div}", department=dept_cp15, semester=sem_5)
            Batch.objects.get_or_create(name=f"M3 - {div}", department=dept_cp15, semester=sem_6)

        self.stdout.write(self.style.SUCCESS(f"✅ Success! Created Data Successfully{session} for Session: {session.name}"))