from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime

#Users Imports
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from .user import *
from ..constants import *



class ActiveProjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='In Progress')
    
class LandDetail(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="land_details")
    land_area_in_sq_ft = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255,)
    building_in_sq_ft = models.FloatField()
    survey_number = models.CharField(max_length=100, blank=True, null=True)
    building_type = models.CharField(max_length=50, choices=BUILDING_CHOICES)
    is_approved = models.BooleanField(default=False)
    attachemnts = models.FileField(upload_to='land_attachments/', blank=True, null=True)

    def __str__(self):
        return f"Land - {self.survey_number} (Customer: {self.customer.user.username})"
    

class Projects(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="projects")
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='Pending')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    current_phase = models.CharField(max_length=200, blank=True, null=True)

    objects = models.Manager()
    active = ActiveProjectsManager()

    def __str__(self):
        return f"Project: {self.title} with {self.service_provider} (Status: {self.status})"
    
    def validate_phase_transition(current_phase, new_phase):
        allowed_transitions = {
            'Pending': ['In Progress', 'Cancelled'],
            'In Progress': ['Completed', 'Cancelled'],
        }
        if new_phase not in allowed_transitions.get(current_phase, []):
            raise ValueError(f"Invalid transition from {current_phase} to {new_phase}")
    
    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def next_phase(self, phase_name):
        self.current_phase = phase_name
        self.save()


class Quotation(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='quotations')
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotation_providers')
    stage = models.CharField(max_length=50, default='General')
    details = models.TextField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Quotation {self.id} for {self.project.title} - Service Provider: {self.service_provider.username} at {self.stage}"
    

class Drawing(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="drawings")
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE, related_name="uploaded_drawings")
    version = models.PositiveIntegerField(default=1)
    file = models.FileField(upload_to='drawings/')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Drawing V{self.version} for {self.project.title}"
    

class Revision(models.Model):
    drawing = models.ForeignKey(Drawing, on_delete=models.CASCADE, related_name="revisions")
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="requested_revisions")
    comment = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Revision Request for Drawing {self.drawing.id}"

class Phase(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="phases")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')
    documents = models.ManyToManyField('Document', blank=True)


class Document(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, blank=True, null=True, related_name="documents")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_documents")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="documents/%Y/%m/%d/")
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Document: {self.description or self.file.name}"
    

#----------------------------------------------------End Projects Model-----------------------------------------------