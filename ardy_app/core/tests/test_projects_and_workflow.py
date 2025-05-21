# core/tests/test_projects_and_workflow.py

import uuid
import itertools
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify

# Adjust these imports based on your exact model and serializer locations
from ..models.user import User, CustomerProfile, ConsultantProfile, ConstructionProfile # Import other SP profiles as needed
from ..models.project import Projects, Phase, Quotation, LandDetail, Drawing, Revision, Document
from ..serializers import ProjectsSerializer, PhaseSerializer, QuotationSerializer # Import other serializers

# Import constants
from ..constants import STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ACCEPTED, STATUS_REJECTED, STATUS_CANCELLED

# --- Test Utility Functions (from test_users_and_auth.py or a common test_utils.py) ---
# It's good practice to move create_test_user to a shared utility if used across multiple test files.
# For this example, I'll assume it's accessible or re-defined if needed.

# Global counter for unique phone numbers in tests (if not in a shared util)
# phone_id_counter_projects_workflow = itertools.count(start=100) # Start from a different range
phone_id_counter_projects_workflow = itertools.count(start=200) # Ensure a different range if running all test files together

def create_test_user_for_workflow(username_prefix="testuser_wf", email_prefix="test_wf", user_type="Customer", password="testpassword123", make_unique=True, **extra_fields):
    unique_suffix = ""
    if make_unique:
        unique_suffix = f"_{uuid.uuid4().hex[:6]}"
    username = f"{username_prefix}{unique_suffix}"
    email = f"{email_prefix}{unique_suffix}@example.com"
    
    phone = extra_fields.pop('phone', None)
    if phone is None:
        # Use a fresh counter or ensure no overlap with other test files if running all tests together
        # For simplicity, assuming a local counter for this hypothetical file.
        # In reality, ensure true uniqueness if tests run in parallel or share DB state in complex ways.
        # unique_id = next(phone_id_counter_projects_workflow)
        unique_id = uuid.uuid4().hex[:7] # Just using uuid for simplicity here
        phone_suffix_6_digit = str(int(unique_id, 16))[-6:].zfill(6) # Example
        phone = f"+97150{phone_suffix_6_digit}"
    
    return User.objects.create_user(
        username=username, email=email, password=password, user_type=user_type, phone=phone, **extra_fields
    )

# --- ProjectsViewSet Tests ---
class ProjectsViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = create_test_user_for_workflow(username_prefix="proj_cust_pv", user_type="Customer")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)

        self.consultant_user = create_test_user_for_workflow(username_prefix="proj_sp_pv", user_type="Consultant")
        self.consultant_profile = ConsultantProfile.objects.get(user=self.consultant_user)
        
        self.construction_user = create_test_user_for_workflow(username_prefix="proj_builder_pv", user_type="Construction")

        self.land_detail = LandDetail.objects.create(customer=self.customer_profile, land_area_in_sq_ft=1000, building_in_sq_ft=500, location="Test Location", building_type="Villa")
        
        self.project1 = Projects.objects.create(
            customer=self.customer_profile, 
            title="Workflow Project One", 
            land_detail=self.land_detail,
            primary_service_provider=self.consultant_user
        )
        self.phase1_p1 = Phase.objects.create(project=self.project1, title="P1 Design", order=1, service_provider=self.consultant_user)
        self.phase2_p1 = Phase.objects.create(project=self.project1, title="P1 Build", order=2) # No SP initially

        self.other_customer_user = create_test_user_for_workflow(username_prefix="other_cust_pv", user_type="Customer")


    def test_list_projects_as_customer(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming no pagination for simplicity or check response.data['count']
        self.assertEqual(len(response.data), 1) 
        self.assertEqual(response.data[0]['title'], "Workflow Project One")

    def test_list_projects_as_sp_assigned_to_phase(self):
        self.client.force_authenticate(user=self.consultant_user) # Consultant is SP for phase1_p1 and primary for project1
        url = reverse('core:project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_projects_as_unrelated_sp(self):
        unrelated_sp = create_test_user_for_workflow(username_prefix="unrelated_sp", user_type="Consultant")
        self.client.force_authenticate(user=unrelated_sp)
        url = reverse('core:project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_customer_creates_project(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:project-list')
        land2 = LandDetail.objects.create(customer=self.customer_profile, land_area_in_sq_ft=2000, building_in_sq_ft=1000, location="New Location", building_type="Building")
        data = {
            "title": "Customer New Project",
            "description": "Details here.",
            "land_detail": land2.pk, # Link to LandDetail
            "primary_service_provider": self.consultant_user.pk # Optional
        }
        response = self.client.post(url, data, format='json')
        # print(f"Create Project Response: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content.decode())
        self.assertEqual(Projects.objects.count(), 2)
        self.assertEqual(response.data['title'], "Customer New Project")

    def test_sp_cannot_create_project(self):
        self.client.force_authenticate(user=self.consultant_user)
        url = reverse('core:project-list')
        data = {"title": "SP Project Attempt"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_project_as_owner_customer(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:project-detail', kwargs={'pk': self.project1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.project1.pk)

    def test_retrieve_project_as_assigned_sp(self):
        self.client.force_authenticate(user=self.consultant_user) # consultant is primary and on phase1
        url = reverse('core:project-detail', kwargs={'pk': self.project1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_project_as_other_customer_fails(self):
        self.client.force_authenticate(user=self.other_customer_user)
        url = reverse('core:project-detail', kwargs={'pk': self.project1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # get_queryset filters it out

    # --- Test Project Actions ---
    def test_customer_starts_project(self):
        self.client.force_authenticate(user=self.customer_user)
        # self.phase1_p1 already has consultant_user as SP
        url = reverse('core:project-start', kwargs={'pk': self.project1.pk})
        # Can optionally pass 'initial_phase_id' in data if not relying on default first phase
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.status, STATUS_IN_PROGRESS)
        self.assertEqual(self.project1.active_phase, self.phase1_p1)

    def test_customer_advances_project_phase(self):
        self.project1.start_project(initial_phase=self.phase1_p1) # Start it first
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:project-advance-phase', kwargs={'pk': self.project1.pk})
        data = {
            "target_phase_id": self.phase2_p1.pk,
            "service_provider_id": self.construction_user.pk # Assigning new SP for build phase
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.project1.refresh_from_db()
        self.phase1_p1.refresh_from_db()
        self.phase2_p1.refresh_from_db()
        self.assertEqual(self.project1.active_phase, self.phase2_p1)
        self.assertEqual(self.phase1_p1.status, STATUS_COMPLETED)
        self.assertEqual(self.phase2_p1.status, STATUS_IN_PROGRESS)
        self.assertEqual(self.phase2_p1.service_provider, self.construction_user)

    @patch('core.models.project.send_mail') # Path to send_mail in project model file
    def test_customer_completes_project(self, mock_send_mail):
        # Setup: complete all phases
        self.project1.start_project(initial_phase=self.phase1_p1)
        self.project1.complete_phase(self.phase1_p1)
        self.phase2_p1.service_provider = self.construction_user
        self.phase2_p1.save()
        self.project1.advance_to_phase(self.phase2_p1)
        self.project1.complete_phase(self.phase2_p1) # This should trigger project completion via signal/method logic

        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:project-complete', kwargs={'pk': self.project1.pk})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.status, STATUS_COMPLETED)
        self.assertGreaterEqual(mock_send_mail.call_count, 1) # At least one email to customer


# --- PhaseViewSet Tests ---
class PhaseViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = create_test_user_for_workflow(username_prefix="phase_cust_pv", user_type="Customer")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)
        self.sp_user = create_test_user_for_workflow(username_prefix="phase_sp_pv", user_type="Consultant")
        
        self.project = Projects.objects.create(customer=self.customer_profile, title="Project for Phase Testing")
        self.phase1 = Phase.objects.create(project=self.project, title="Phase One", order=1, service_provider=self.sp_user)

    def test_customer_creates_phase_for_their_project(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:phase-list')
        data = {
            "project": self.project.pk,
            "title": "Phase Two by Customer",
            "order": 2,
            "service_provider": self.sp_user.pk # Customer can assign SP
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content.decode())
        self.assertEqual(self.project.phases.count(), 2)

    def test_sp_cannot_create_phase_for_project(self):
        self.client.force_authenticate(user=self.sp_user) # SP assigned to phase1
        url = reverse('core:phase-list')
        data = {"project": self.project.pk, "title": "SP Creates Phase", "order": 3}
        response = self.client.post(url, data, format='json')
        # Assuming your perform_create for PhaseViewSet restricts creation to project customer/admin
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 

    def test_list_phases_for_a_project(self):
        self.client.force_authenticate(user=self.customer_user)
        Phase.objects.create(project=self.project, title="Phase Alpha", order=0)
        url = reverse('core:phase-list') + f'?project_id={self.project.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # phase1 + Phase Alpha

    def test_sp_completes_assigned_phase(self):
        self.project.start_project(initial_phase=self.phase1) # Phase1 is 'In Progress'
        self.client.force_authenticate(user=self.sp_user) # sp_user is assigned to phase1
        url = reverse('core:phase-complete-phase-action', kwargs={'pk': self.phase1.pk})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.phase1.refresh_from_db()
        self.assertEqual(self.phase1.status, STATUS_COMPLETED)

    def test_customer_completes_phase(self): # Customers can also mark phase as complete
        self.project.start_project(initial_phase=self.phase1)
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:phase-complete-phase-action', kwargs={'pk': self.phase1.pk})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.phase1.refresh_from_db()
        self.assertEqual(self.phase1.status, STATUS_COMPLETED)

    def test_unrelated_sp_cannot_complete_phase(self):
        unrelated_sp = create_test_user_for_workflow(username_prefix="unrelated_sp_phase", user_type="Consultant")
        self.project.start_project(initial_phase=self.phase1)
        self.client.force_authenticate(user=unrelated_sp)
        url = reverse('core:phase-complete-phase-action', kwargs={'pk': self.phase1.pk})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# --- QuotationViewSet Tests (Focus on actions and permissions, CRUD is standard) ---
class QuotationViewSetWorkflowTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = create_test_user_for_workflow(username_prefix="quote_cust_pv", user_type="Customer")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)
        self.sp_user = create_test_user_for_workflow(username_prefix="quote_sp_pv", user_type="Consultant")
        
        self.project = Projects.objects.create(customer=self.customer_profile, title="Project for Quotations")
        self.phase = Phase.objects.create(project=self.project, title="Design Phase", order=1, service_provider=self.sp_user)
        self.quotation = Quotation.objects.create(
            project=self.project, phase=self.phase, service_provider=self.sp_user, 
            type="Initial Design Quote", amount=1500, status=STATUS_PENDING
        )

    def test_sp_creates_quotation(self): # Basic creation was likely tested with model methods
        self.client.force_authenticate(user=self.sp_user)
        url = reverse('core:quotation-list')
        data = {
            "project": self.project.pk,
            "phase": self.phase.pk, # or phase_id if your serializer uses that
            "type": "Revision Quote",
            "amount": "500.00",
            "details": "For additional revisions."
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content.decode())
        self.assertEqual(self.project.quotations.count(), 2)

    @patch('core.models.project.send_mail') # Path to send_mail in project model file (Quotation model)
    def test_customer_approves_quotation(self, mock_send_mail):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:quotation-approve', kwargs={'pk': self.quotation.pk})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.quotation.refresh_from_db()
        self.assertEqual(self.quotation.status, STATUS_ACCEPTED)
        mock_send_mail.assert_called_once() # Check if notification was sent

    def test_customer_rejects_quotation(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:quotation-reject', kwargs={'pk': self.quotation.pk})
        response = self.client.post(url, {"reason": "Too costly"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.quotation.refresh_from_db()
        self.assertEqual(self.quotation.status, STATUS_REJECTED)

    def test_sp_cannot_approve_own_quotation(self):
        self.client.force_authenticate(user=self.sp_user)
        url = reverse('core:quotation-approve', kwargs={'pk': self.quotation.pk})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
def create_test_user_for_workflow(username_prefix="testuser_wf", email_prefix="test_wf", user_type="Customer", password="testpassword123", make_unique=True, **extra_fields):
    unique_suffix = ""
    if make_unique:
        unique_suffix = f"_{uuid.uuid4().hex[:6]}"
    username = f"{username_prefix}{unique_suffix}"
    email = f"{email_prefix}{unique_suffix}@example.com"
    
    phone = extra_fields.pop('phone', None)
    if phone is None:
        unique_id = next(phone_id_counter_projects_workflow)
        phone_suffix_6_digit = str(unique_id).zfill(6)
        if len(phone_suffix_6_digit) > 6:
            phone_suffix_6_digit = phone_suffix_6_digit[-6:]
        phone = f"+97150{phone_suffix_6_digit}"
    
    return User.objects.create_user(
        username=username, email=email, password=password, user_type=user_type, phone=phone, **extra_fields
    )

# --- ProjectsViewSet Tests (Keep existing tests) ---
class ProjectsViewSetTests(APITestCase):
    # ... (all your existing setUp and test methods for ProjectsViewSet) ...
    pass


# --- PhaseViewSet Tests (Keep existing tests) ---
class PhaseViewSetTests(APITestCase):
    # ... (all your existing setUp and test methods for PhaseViewSet) ...
    pass


# --- QuotationViewSet Tests (Keep existing tests, renamed class for clarity) ---
class QuotationViewSetWorkflowTests(APITestCase): # Renamed from QuotationViewSetTests
    # ... (all your existing setUp and test methods for QuotationViewSetWorkflowTests) ...
    pass


# --- DrawingViewSet Tests ---
class DrawingViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = create_test_user_for_workflow(username_prefix="draw_cust", user_type="Customer")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)
        
        self.consultant_user = create_test_user_for_workflow(username_prefix="draw_consult", user_type="Consultant")
        self.consultant_profile = ConsultantProfile.objects.get(user=self.consultant_user) # Used if Drawing.uploaded_by_consultant is used

        self.project = Projects.objects.create(customer=self.customer_profile, title="Project for Drawings")
        self.phase = Phase.objects.create(project=self.project, title="Design Phase for Drawings", order=1, service_provider=self.consultant_user)

        # A dummy file for upload tests
        self.dummy_file = SimpleUploadedFile("test_drawing.pdf", b"file_content", content_type="application/pdf")
        self.list_create_url = reverse('core:drawing-list')

    def test_consultant_uploads_drawing_to_phase(self):
        self.client.force_authenticate(user=self.consultant_user)
        current_dummy_file = SimpleUploadedFile("test_drawing.pdf", b"file_content", content_type="application/pdf")
        data = {
            "project": self.project.pk,
            "phase": self.phase.pk,
            "title": "Initial Concept Drawing",
            "notes": "First draft",
            "file": current_dummy_file
        }
        response = self.client.post(self.list_create_url, data, format='multipart') # Use 'multipart' for file uploads
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content.decode())
        self.assertEqual(Drawing.objects.count(), 1)
        drawing = Drawing.objects.first()
        self.assertEqual(drawing.title, "Initial Concept Drawing")
        self.assertEqual(drawing.uploaded_by, self.consultant_user) # Assuming perform_create sets this
        self.assertTrue(drawing.file.name.startswith(f"projects/{self.project.pk}/drawings/v{drawing.version}_"))
        # Check for either _ or - in the slugified part, depending on default slugify behavior
        self.assertTrue(
            f"test_drawing" in drawing.file.name.lower() or \
            f"test-drawing" in drawing.file.name.lower()
        )
        self.assertTrue(drawing.file.name.lower().endswith(".pdf"))

    @patch('core.signals.send_mail') # Assuming a signal sends email on new drawing
    def test_drawing_upload_notifies_customer(self, mock_send_mail):
        self.client.force_authenticate(user=self.consultant_user)
        data = {"project": self.project.pk, "phase": self.phase.pk, "title": "Notification Drawing", "file": self.dummy_file}
        self.client.post(self.list_create_url, data, format='multipart')
        self.assertEqual(Drawing.objects.count(), 1)
        # Check if the signal for new drawing notification was triggered
        customer_notified = False
        for call_args_tuple in mock_send_mail.call_args_list:
            _, kwargs = call_args_tuple
            if self.customer_user.email in kwargs.get('recipient_list', []):
                self.assertIn("New Drawing Uploaded", kwargs.get('subject', ''))
                customer_notified = True
                break
        self.assertTrue(customer_notified, "Customer was not notified of new drawing upload.")


    def test_customer_cannot_upload_drawing(self):
        self.client.force_authenticate(user=self.customer_user)
        data = {"project": self.project.pk, "phase": self.phase.pk, "title": "Customer Drawing", "file": self.dummy_file}
        response = self.client.post(self.list_create_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Assuming DrawingViewSet.perform_create checks user type

    def test_list_drawings_for_project_as_customer(self):
        Drawing.objects.create(project=self.project, phase=self.phase, uploaded_by=self.consultant_user, title="D1", file=self.dummy_file)
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.list_create_url, {'project_id': self.project.pk}) # Assuming filtering by project_id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "D1")

    def test_unauthenticated_cannot_list_drawings(self):
        response = self.client.get(self.list_create_url, {'project_id': self.project.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Or 403

# --- RevisionViewSet Tests ---
class RevisionViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = create_test_user_for_workflow(username_prefix="rev_cust", user_type="Customer")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)
        
        self.consultant_user = create_test_user_for_workflow(username_prefix="rev_consult", user_type="Consultant")

        self.project = Projects.objects.create(customer=self.customer_profile, title="Project for Revisions")
        self.phase = Phase.objects.create(project=self.project, title="Design Phase for Revisions", order=1, service_provider=self.consultant_user)
        
        dummy_file = SimpleUploadedFile("drawing_for_rev.pdf", b"content", content_type="application/pdf")
        self.drawing = Drawing.objects.create(
            project=self.project, phase=self.phase, uploaded_by=self.consultant_user, 
            title="Drawing To Be Revised", file=dummy_file
        )
        self.list_create_url = reverse('core:revision-list')

    def test_customer_requests_revision_for_drawing_on_own_project(self):
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "drawing": self.drawing.pk,
            "comment": "Please change the color to blue."
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content.decode())
        self.assertEqual(Revision.objects.count(), 1)
        revision = Revision.objects.first()
        self.assertEqual(revision.customer, self.customer_profile)
        self.assertEqual(revision.comment, "Please change the color to blue.")

    @patch('core.signals.send_mail') # Assuming signal sends email on new revision request
    def test_revision_request_notifies_uploader(self, mock_send_mail):
        self.client.force_authenticate(user=self.customer_user)
        data = {"drawing": self.drawing.pk, "comment": "Notification test comment."}
        self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(Revision.objects.count(), 1)

        uploader_notified = False
        for call_args_tuple in mock_send_mail.call_args_list:
            _, kwargs = call_args_tuple
            if self.consultant_user.email in kwargs.get('recipient_list', []): # Consultant uploaded the drawing
                self.assertIn("Revision Requested", kwargs.get('subject', ''))
                uploader_notified = True
                break
        self.assertTrue(uploader_notified, "Drawing uploader was not notified of new revision request.")

    def test_consultant_cannot_request_revision(self): # SPs don't request revisions, customers do
        self.client.force_authenticate(user=self.consultant_user)
        data = {"drawing": self.drawing.pk, "comment": "SP trying to revise."}
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_request_revision_for_drawing_on_other_project(self):
        other_customer = create_test_user_for_workflow(username_prefix="other_rev_cust", user_type="Customer")
        # Drawing belongs to self.customer_user's project
        self.client.force_authenticate(user=other_customer)
        data = {"drawing": self.drawing.pk, "comment": "Trying to revise other's drawing."}
        response = self.client.post(self.list_create_url, data, format='json')
        # This depends on perform_create logic in RevisionViewSet to check drawing ownership
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Or 400 if validation error

    def test_consultant_lists_revisions_for_their_drawings(self):
        Revision.objects.create(drawing=self.drawing, customer=self.customer_profile, comment="Rev 1")
        self.client.force_authenticate(user=self.consultant_user) # Consultant who uploaded the drawing
        response = self.client.get(self.list_create_url, {'drawing_id': self.drawing.pk}) # Assuming filtering
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['comment'], "Rev 1")


# TODO:
# - DocumentViewSetTests:
#   - Similar structure: setUp users, project, phase.
#   - test_customer_uploads_project_document (e.g., land survey)
#   - test_sp_uploads_phase_document (e.g., material spec for their phase)
#   - test_list_documents_permissions (who sees what)
#   - test_unauthorized_upload_delete
# - Flesh out update/delete tests for DrawingViewSet, RevisionViewSet, DocumentViewSet with permissions.
# - Add tests for retrieving single instances (detail views) for these viewsets.
# - Add more specific permission failure tests for each action in all viewsets.
# - Test any custom actions you add to these viewsets.