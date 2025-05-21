# core/models/project.py
from django.db import models, transaction
from django.utils import timezone
from django.utils.text import slugify
from django.core.mail import send_mail

#Users Imports
from .user import *
from ..constants import *

class ActiveProjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='In Progress')
    
def land_attachment_upload_path(instance, filename):
    username_slug = slugify(instance.customer.user.username)
    project_id_str = str(instance.id) if instance.id else "new_land_details"
    return os.path.join('land_attachments', username_slug, project_id_str, filename)

def drawing_upload_path(instance, filename):
    project_id_str = str(instance.project_id)
    name, ext = os.path.splitext(filename)
    slugified_name = slugify(name)
    final_filename_part = f"v{instance.version}_{slugified_name}{ext.lower()}"
    return os.path.join('projects', project_id_str, "drawings", final_filename_part)

def general_document_upload_path(instance, filename):
    project_id_str = str(instance.project_id) if instance.project_id else "general_documents"
    uploaded_by_slug = slugify(instance.uploaded_by.username)
    date_path = timezone.now().strftime("%Y/%m/%d")
    return os.path.join('documents', project_id_str, uploaded_by_slug, date_path, slugify(filename))
    
class LandDetail(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="land_details")
    land_area_in_sq_ft = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    building_in_sq_ft = models.DecimalField(max_digits=10, decimal_places=2)
    survey_number = models.CharField(max_length=100, blank=True, null=True)
    building_type = models.CharField(max_length=50, choices=BUILDING_CHOICES)
    is_approved = models.BooleanField(default=False)
    attachments = models.FileField(upload_to=land_attachment_upload_path, blank=True, null=True)

    def __str__(self):
        return f"Land {self.id} - {self.survey_number or 'N/A'} (Customer: {self.customer.user.username})"
    

class Projects(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="projects")
    primary_service_provider = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="primary_projects", help_text="Main Service Provider if project is simple")
    land_detail = models.OneToOneField(LandDetail, on_delete=models.SET_NULL, blank=True, null=True, related_name="project")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default=STATUS_PENDING)
    active_phase = models.ForeignKey('Phase', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', help_text='The currently active phase of the project')
    start_date = models.DateTimeField(default=timezone.now)
    expected_end_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)
    
    
    objects = models.Manager()
    active = ActiveProjectsManager()

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = 'Projects'
        
    def __str__(self):
        provider_info = "N/A"
        current_sp = self.get_current_service_provider()
        if current_sp:
            provider_info = current_sp.username
        elif self.primary_service_provider:
            provider_info = self.primary_service_provider.username
        return f"Project: {self.id}: {self.title} (Customer: {self.customer.user.username}) with {provider_info} (Status: {self.get_status_display()})"
    

    def _can_transition_project_status(self, new_status):
        # Basic linear progression, disallow going backwards from completed/cancelled
        if self.status in [STATUS_COMPLETED, STATUS_CANCELLED] and new_status != self.status:
            return False, f"Project is already {self.get_status_display()} and cannot be changed to {new_status}."

        # Example: Cannot move to 'In Progress' if no phases are defined or no active phase.
        if new_status == STATUS_IN_PROGRESS and not self.phases.exists():
            return False, "Project cannot be set to 'In Progress' without any defined phases."

        # Add more rules as needed
        return True, ""

    def _can_transition_phase_status(self, phase, new_status):
        """
        Validates if a specific phase can transition to a new status.
        """
        if phase.status in [STATUS_COMPLETED, STATUS_CANCELLED] and new_status != phase.status:
            return False, f"Phase '{phase.title}' is already {phase.get_status_display()}."

        # Example: Phase cannot be 'In Progress' if its service provider is not set
        if new_status == STATUS_IN_PROGRESS and not phase.service_provider:
            return False, f"Phase '{phase.title}' cannot start without an assigned service provider."

        return True, ""


    @transaction.atomic
    def start_project(self, initial_phase=None):
        """
        Officially starts the project.
        Sets the project status to 'In Progress'.
        Sets the initial_phase as active if provided and valid, otherwise finds the first phase by order.
        """
        can_transition, msg = self._can_transition_project_status(STATUS_IN_PROGRESS)
        if not can_transition:
            raise ValueError(f"Cannot start project: {msg}")

        if self.status == STATUS_IN_PROGRESS:
            # Idempotency: if already in progress and trying to start with the same active phase, do nothing
            if initial_phase and self.active_phase == initial_phase:
                return
            # Or raise error if already started differently
            # raise ValueError("Project is already in progress.")

        if initial_phase:
            if not initial_phase.project == self:
                raise ValueError("Initial phase does not belong to this project.")
            if not initial_phase.service_provider:
                raise ValueError(f"Phase '{initial_phase.title}' cannot be started without a service provider.")
            self.active_phase = initial_phase
        else:
            # Find the first phase by order if no specific initial_phase is given
            first_phase = self.phases.order_by('order').first()
            if not first_phase:
                raise ValueError("Project has no phases defined. Cannot start.")
            if not first_phase.service_provider:
                raise ValueError(f"Initial phase '{first_phase.title}' cannot be started without a service provider.")
            self.active_phase = first_phase

        self.status = STATUS_IN_PROGRESS
        if not self.start_date or self.start_date.date() > timezone.now().date(): # if start_date was future or not set
            self.start_date = timezone.now()

        if self.active_phase.status == STATUS_PENDING:
            self.active_phase.status = STATUS_IN_PROGRESS
            if not self.active_phase.start_date:
                self.active_phase.start_date = timezone.now()
            self.active_phase.save()

        self.save()
        # TODO: Create notifications: Project started, Phase X started.

    @transaction.atomic
    def advance_to_phase(self, target_phase, new_service_provider_for_target_phase=None):
        """
        Advances the project to a specified target_phase.
        Completes the current active_phase (if any and not already completed).
        Sets the target_phase as active and 'In Progress'.
        Optionally assigns/updates the service_provider for the target_phase.
        """
        if not target_phase.project == self:
            raise ValueError("Target phase does not belong to this project.")

        if self.active_phase == target_phase and self.active_phase.status == STATUS_IN_PROGRESS:
            # raise ValueError("Project is already active in the target phase.")
            return # Idempotent if already in this state

        # Assign service provider to the target phase if provided
        if new_service_provider_for_target_phase:
            target_phase.service_provider = new_service_provider_for_target_phase
            # No save here, will be saved as part of phase status update or below

        if not target_phase.service_provider:
            raise ValueError(f"Target phase '{target_phase.title}' cannot be started without an assigned service provider.")

        current_active_phase = self.active_phase

        # Complete the current active phase if it exists and is not already completed/cancelled
        if current_active_phase and current_active_phase.status not in [STATUS_COMPLETED, STATUS_CANCELLED]:
            current_active_phase.status = STATUS_COMPLETED
            if not current_active_phase.actual_end_date:
                current_active_phase.actual_end_date = timezone.now()
            current_active_phase.save()
            # TODO: Create notification: Phase X completed.

        # Activate the target phase
        self.active_phase = target_phase
        if target_phase.status == STATUS_PENDING: # Only set to In Progress if it was Pending
            target_phase.status = STATUS_IN_PROGRESS
            if not target_phase.start_date: # Set start date if not already set
                target_phase.start_date = timezone.now()
        # If target_phase was already 'In Progress' or 'Completed', its status remains.
        # If it was 'Cancelled', this might be an issue - decide policy.
        if target_phase.status == STATUS_CANCELLED:
            raise ValueError(f"Cannot advance to a cancelled phase: '{target_phase.title}'.")

        target_phase.save() # Save changes to target_phase (SP, status, start_date)

        # Update project status if it's not already 'In Progress'
        if self.status != STATUS_IN_PROGRESS:
            can_transition, msg = self._can_transition_project_status(STATUS_IN_PROGRESS)
            if not can_transition:
                raise ValueError(f"Cannot set project to In Progress: {msg}")
            self.status = STATUS_IN_PROGRESS

        self.save()
        # TODO: Create notifications: Project advanced to Phase Y, Phase Y started.

    @transaction.atomic
    def complete_phase(self, phase_to_complete):
        """
        Marks a specific phase as completed.
        """
        if not phase_to_complete.project == self:
            raise ValueError("Phase does not belong to this project.")

        if phase_to_complete.status == STATUS_COMPLETED:
            return # Idempotent

        can_transition, msg = self._can_transition_phase_status(phase_to_complete, STATUS_COMPLETED)
        if not can_transition:
            raise ValueError(f"Cannot complete phase '{phase_to_complete.title}': {msg}")

        phase_to_complete.status = STATUS_COMPLETED
        if not phase_to_complete.actual_end_date:
            phase_to_complete.actual_end_date = timezone.now()
        phase_to_complete.save()
        # TODO: Create notification: Phase X completed.

        # Optional: Check if this completion triggers project completion
        # self.check_and_complete_project_if_all_phases_done()


    @transaction.atomic
    def complete_project(self, force_complete=False):
        """
        Marks the entire project as completed.
        Ensures all active phases are completed (unless force_complete is True).
        """
        if self.status == STATUS_COMPLETED:
            return # =
        if not force_complete:
            # Check if there's an active phase that isn't completed
            if self.active_phase and self.active_phase.status not in [STATUS_COMPLETED, STATUS_CANCELLED]:
                raise ValueError(f"Cannot complete project. Active phase '{self.active_phase.title}' is not yet completed.")

            # Check if any other non-active phases are still pending or in progress
            incomplete_phases = self.phases.exclude(status__in=[STATUS_COMPLETED, STATUS_CANCELLED]).exists()
            if incomplete_phases:
                # Example: find one such phase to report
                offending_phase = self.phases.exclude(status__in=[STATUS_COMPLETED, STATUS_CANCELLED]).first()
                raise ValueError(f"Cannot complete project. At least one phase ('{offending_phase.title}') is not yet completed or cancelled.")

        can_transition, msg = self._can_transition_project_status(STATUS_COMPLETED)
        if not can_transition:
            raise ValueError(f"Cannot complete project: {msg}")

        self.status = STATUS_COMPLETED
        self.active_phase = None # No single phase is active once project is completed
        if not self.actual_end_date:
            self.actual_end_date = timezone.now()
        self.save()
        try:
            customer_user = self.customer.user
            send_mail(
                subject=f"Your Project '{self.title}' is Complete!",
                message=f"Dear {customer_user.first_name or customer_user.username}, \n\nYour project '{self.title}' has been marked as completed.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_user.email],
                fail_silently=False,
            )
            if self.primary_service_provider and self.primary_service_provider.email:
                send_mail(
                    subject=f"Project '{self.title}' Marked as Complete",
                    message=f"Dear {self.primary_service_provider.first_name or self.primary_service_provider.username},\n\nThe project '{self.title}' (Customer: {customer_user.username}) has been marked as completed.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.primary_service_provider.email],
                    fail_silently=False,
                )
                
        except AttributeError as e:
            print(f"Error sending project completion notification for Project ID {self.id} (AttributeError): {e}")
        except Exception as e:
            print(f"General error sending project completion notification for Project ID {self.id}: {e}")
        # TODO: Trigger final payment releases, etc.

    @transaction.atomic
    def cancel_project(self, reason=""):
        """
        Cancels the entire project.
        Optionally sets active phase to cancelled.
        """
        can_transition, msg = self._can_transition_project_status(STATUS_CANCELLED)
        if not can_transition:
            raise ValueError(f"Cannot cancel project: {msg}")

        # Optionally handle the active phase
        if self.active_phase and self.active_phase.status not in [STATUS_COMPLETED, STATUS_CANCELLED]:
            self.active_phase.status = STATUS_CANCELLED
            # self.active_phase.cancellation_reason = reason # if you add such a field
            if not self.active_phase.actual_end_date: # A cancelled phase also "ends"
                self.active_phase.actual_end_date = timezone.now()
            self.active_phase.save()

        self.status = STATUS_CANCELLED
        # self.cancellation_reason = reason # if you add such a field to Project model
        if not self.actual_end_date: # A cancelled project also "ends"
            self.actual_end_date = timezone.now()
        self.save()
        # TODO: Create notifications: Project Cancelled.
        # TODO: Handle any financial implications of cancellation.

    # Helper to be called after a phase is completed.
    def check_and_complete_project_if_all_phases_done(self):
        """
        Checks if all phases of the project are completed or cancelled.
        If so, and the project is not already completed, completes the project.
        """
        if self.status == STATUS_COMPLETED:
            return

        all_phases_terminal = not self.phases.exclude(status__in=[STATUS_COMPLETED, STATUS_CANCELLED]).exists()
        if all_phases_terminal:
            try:
                self.complete_project()
            except ValueError:
                # This might happen if complete_project has other pre-conditions not met. Log it.
                print(f"Project {self.id}: All phases terminal, but project completion failed.")
    

class Phase(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="phases")
    service_provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_phases", help_text="Service Provider assigned to this phase")
    title = models.CharField(max_length=255, help_text="e.g Design, Foundation, Electrical Work")
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Execution order of the phase")
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_PENDING)
    start_date = models.DateTimeField(null=True, blank=True)
    expected_end_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['project', 'order']
        unique_together = [['project', 'order']]
        
    def __str__(self):
        provider_username = self.service_provider.username if self.service_provider else "Unassigned"
        return f"Phase ({self.id}): {self.title} for Project {self.project.id} (Service Provider: {provider_username}, Status: {self.get_status_display()})"
    
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old_status = None
        if not is_new:
            try:
                # Get status before save
                old_status = Phase.objects.get(pk=self.pk).status
            except Phase.DoesNotExist:
                pass
            
        super().save(*args, **kwargs)
        
        if self.status == STATUS_COMPLETED and (is_new or old_status != STATUS_COMPLETED):
            if self.project:
                self.project.check_and_complete_project_if_all_phases_done()

class Quotation(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='quotations')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='quotations', null=True, blank=True, help_text="Quotation for specific phase")
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_quotations')
    type = models.CharField(max_length=100, default="Initial Quotation" ,  help_text="e.g Initial Design, Construction Bid")
    details = models.TextField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        phase_title = f" for Phase: {self.phase.title}" if self.phase else ""
        return f"Quotation {self.id} for Project {self.project.title} {phase_title} - Service Provider: {self.service_provider.username}"
    
    def _can_transition_status(self, new_status):
        if self.status not in [STATUS_PENDING]:
            return False, f"Quotation is already {self.get_status_display()} and cannot be changed."
        if new_status not in [STATUS_ACCEPTED, STATUS_REJECTED]:
            return False, f"Invalid target status '{new_status}' for quotation."
        return True, ""
    
    @transaction.atomic
    def approve(self, approving_user): # Pass the user who is approving
        """ Approves the quotation. """
        can_transition, msg = self._can_transition_status(STATUS_ACCEPTED)
        if not can_transition:
            raise ValueError(msg)

        self.status = STATUS_ACCEPTED
        self.approved_at = timezone.now() 
        self.save()

        try:
            provider_email = self.service_provider.email
            message_body = (
                f"Dear {self.service_provider.first_name or self.service_provider.username},\n\n"
                f"Your quotation of type '{self.type}' for project '{self.project.title}' "
                f"(Customer: {self.project.customer.user.username}) has been APPROVED.\n\n"
                f"Approved by: {approving_user.username}"
            )
            send_mail(
                subject=f"Quotation Approved: {self.type} for Project {self.project.title}",
                message=message_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[provider_email],
                fail_silently=False,
            )
            # TODO: Trigger payment process for this quotation if applicable
        except AttributeError as e:
            print(f"Error sending quotation approval notification for Quotation ID {self.id} (AttributeError): {e}")
        except Exception as e:
            print(f"General error sending quotation approval notification for Quotation ID {self.id}: {e}")
        # --- End Notification Logic ---

    @transaction.atomic
    def reject(self, rejecting_user, reason=""): # Pass user and optional reason
        """ Rejects the quotation. """
        can_transition, msg = self._can_transition_status(STATUS_REJECTED)
        if not can_transition:
            raise ValueError(msg)

        self.status = STATUS_REJECTED
        self.rejection_reason = reason # If you add such a field
        self.save()

        # --- Notification Logic Moved Here ---
        try:
            provider_email = self.service_provider.email
            message_body = (
                f"Dear {self.service_provider.first_name or self.service_provider.username},\n\n"
                f"Your quotation of type '{self.type}' for project '{self.project.title}' "
                f"(Customer: {self.project.customer.user.username}) has been REJECTED.\n\n"
                f"Rejected by: {rejecting_user.username}"
                + (f"\nReason: {reason}" if reason else "")
            )
            send_mail(
                subject=f"Quotation Rejected: {self.type} for Project {self.project.title}",
                message=message_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[provider_email],
                fail_silently=False,
            )
        except AttributeError as e:
            print(f"Error sending quotation rejection notification for Quotation ID {self.id} (AttributeError): {e}")
        except Exception as e:
            print(f"General error sending quotation rejection notification for Quotation ID {self.id}: {e}")
        # --- End Notification Logic ---


class Drawing(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="drawings")
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True, blank=True, related_name="drawings", help_text="Phase this drawing belongs to")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name="uploaded_drawings")
    title = models.CharField(max_length=255,default="Untitled Drawing")
    version = models.PositiveIntegerField(default=1)
    file = models.FileField(upload_to=drawing_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['project', 'phase', '-version']

    def __str__(self):
        return f"Drawing V{self.version} - {self.title} for {self.project.title}"
    
    
class Revision(models.Model):
    drawing = models.ForeignKey(Drawing, on_delete=models.CASCADE, related_name="revisions")
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="requested_revisions")
    comment = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Revision Request ({self.id}) for Drawing {self.drawing.id} (v{self.drawing.version})"
    
    
class Document(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, blank=True, null=True, related_name="project_documents")
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, blank=True, null=True, related_name="phase_documents")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="uploaded_project_documents")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=general_document_upload_path)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        name = self.title or self.file.name.split('/')[-1]
        return f"Document ({self.id}): {name} (Project: {self.project_id})"
    

#----------------------------------------------------End Projects Model-----------------------------------------------