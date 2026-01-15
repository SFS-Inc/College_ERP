from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import Department, Subject


class User(AbstractUser):

    """
    Custom User model for College ERP.

    Roles:=
    Staff: Faculty Members
    Students: Reserved for the fututure can be expanded later and this model is made for that(note to future self)

    Relationships:=
    Department: IT says what department the faculty member belongs to
    Subject: Subjects the faculty teacher

    (Note to future self: Need to change relation to accomodate data for each batch so it shows fresh data each semester)


    """
    STAFF = 'STAFF'
    STUDENT = 'STUDENT'

    ROLE_CHOICES = [
        (STAFF, 'Faculty / Staff'),
        (STUDENT, 'Student'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STAFF
    )

    departments = models.ManyToManyField(
        Department,
        blank=True,
        related_name='faculties'
    )

    subject=models.ManyToManyField(
        Subject,
        blank=True,
        related_name='faculties'
    )

    def __str__(self):
        return self.username