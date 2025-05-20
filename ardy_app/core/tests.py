from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch # For mocking email sending
import itertools

phone_counter = itertools.count(start=1000000000)

# Import your models (adjust paths based on your model structure)
from .models.user import (
    User as UserModel, # Alias to avoid clash with 'User' variable name if any
    CustomerProfile, ConsultantProfile, SubscriptionPlan, UserSubscription,
)
from .models.project import (
    Projects, Phase, Quotation, Drawing, Revision, Document, LandDetail
)
from .models import Referral
# Import constants
from .constants import (
    STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ACCEPTED, STATUS_REJECTED
)

User = get_user_model() # Standard way to get the User model

# --- Test Utility Functions (Optional) ---
def create_user(username="testuser", password="testpassword123", email="test@example.com", user_type="Customer", phone=None, **extra_fields):
    if phone is None:
        # Generate a unique phone number if not provided
        # Ensure it fits your phone_regex if that's strict during User.save()
        # For simplicity, using a basic unique number here. Adjust format as needed.
        unique_phone_suffix = next(phone_counter)
        phone = f"+97150{unique_phone_suffix}" # Example format, adjust to your regex
        # If your phone_regex is very strict, you might need a more sophisticated generator
        # or ensure you always pass a valid, unique phone number to this helper.

    # Ensure email is also unique for subsequent calls if not overridden
    if 'email' not in extra_fields and User.objects.filter(email=email).exists() and username != "testuser":
        base_email, domain = email.split('@')
        email = f"{base_email}_{username}@{domain}"


    print(f"--- Creating user: {username}, Email: {email}, Phone: {phone}, Type: {user_type} ---") # Debug print
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        user_type=user_type,
        phone=phone, # Pass the unique phone number
        **extra_fields
    )

# --- Model Tests ---

class UserModelTests(APITestCase):
    def test_create_user(self):
        user = create_user(user_type="Consultant")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.user_type, "Consultant")
        self.assertTrue(user.check_password("testpassword123"))

    def test_user_profile_signal(self):
        """ Test if profile is created on user creation (via signal) """
        user = create_user(user_type="Customer")
        self.assertTrue(CustomerProfile.objects.filter(user=user).exists())
        user_consultant = create_user(username="consultant1", email="c1@example.com", user_type="Consultant")
        self.assertTrue(ConsultantProfile.objects.filter(user=user_consultant).exists())

    def test_referral_code_signal(self):
        """ Test if referral code is created on user creation """
        user = create_user(username="referrer", email="referrer@example.com")
        self.assertTrue(Referral.objects.filter(referrer=user).exists())
        referral = Referral.objects.get(referrer=user)
        self.assertTrue(referral.code.startswith("REF-"))


class ProjectModelMethodTests(APITestCase):
    def setUp(self):
        self.customer_user = create_user(username="customer1", email="cust1@example.com", user_type="Customer")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user) # Assuming signal created it

        self.consultant_user = create_user(username="consultant1", email="cons1@example.com", user_type="Consultant")
        # self.consultant_profile = ConsultantProfile.objects.get(user=self.consultant_user)

        self.project = Projects.objects.create(
            customer=self.customer_profile,
            title="Test Project Alpha",
            primary_service_provider=self.consultant_user
        )
        self.phase1 = Phase.objects.create(
            project=self.project,
            title="Design Phase",
            order=1,
            service_provider=self.consultant_user
        )
        self.phase2 = Phase.objects.create(
            project=self.project,
            title="Build Phase",
            order=2
            # service_provider will be assigned later in some tests
        )

    def test_start_project(self):
        self.assertEqual(self.project.status, STATUS_PENDING)
        self.project.start_project() # Uses first phase (phase1) by default
        self.project.refresh_from_db()
        self.phase1.refresh_from_db()
        self.assertEqual(self.project.status, STATUS_IN_PROGRESS)
        self.assertEqual(self.project.active_phase, self.phase1)
        self.assertEqual(self.phase1.status, STATUS_IN_PROGRESS)

    def test_start_project_specific_initial_phase(self):
        # Cannot start phase2 yet as it has no service provider
        with self.assertRaises(ValueError):
            self.project.start_project(initial_phase=self.phase2)

        self.phase2.service_provider = self.consultant_user
        self.phase2.save()
        self.project.start_project(initial_phase=self.phase2)
        self.project.refresh_from_db()
        self.phase2.refresh_from_db()
        self.assertEqual(self.project.status, STATUS_IN_PROGRESS)
        self.assertEqual(self.project.active_phase, self.phase2)
        self.assertEqual(self.phase2.status, STATUS_IN_PROGRESS)


    def test_advance_to_phase(self):
        self.project.start_project(initial_phase=self.phase1) # Start with phase1
        
        construction_user = create_user(username="builder1", email="build1@example.com", user_type="Construction")
        self.project.advance_to_phase(self.phase2, new_service_provider_for_target_phase=construction_user)

        self.project.refresh_from_db()
        self.phase1.refresh_from_db()
        self.phase2.refresh_from_db()

        self.assertEqual(self.phase1.status, STATUS_COMPLETED)
        self.assertEqual(self.project.active_phase, self.phase2)
        self.assertEqual(self.phase2.status, STATUS_IN_PROGRESS)
        self.assertEqual(self.phase2.service_provider, construction_user)

    def test_complete_phase(self):
        self.project.start_project(initial_phase=self.phase1)
        self.project.complete_phase(phase_to_complete=self.phase1)
        self.phase1.refresh_from_db()
        self.assertEqual(self.phase1.status, STATUS_COMPLETED)
        # Project itself is not yet completed if phase2 exists and is pending
        self.assertNotEqual(self.project.status, STATUS_COMPLETED)


    def test_complete_project_successfully(self):
        self.project.start_project(initial_phase=self.phase1)
        self.project.complete_phase(phase_to_complete=self.phase1) # phase1 completed

        # Now make phase2 ready and complete it
        self.phase2.service_provider = self.consultant_user
        self.phase2.save()
        self.project.advance_to_phase(self.phase2) # active_phase is now phase2, phase1 is completed
        self.project.complete_phase(phase_to_complete=self.phase2) # phase2 completed

        # check_and_complete_project_if_all_phases_done should have been called by phase.save()
        # or by project.complete_phase()
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, STATUS_COMPLETED)
        self.assertIsNotNone(self.project.actual_end_date)

    def test_complete_project_fails_if_phase_not_done(self):
        self.project.start_project(initial_phase=self.phase1)
        # phase1 is In Progress, phase2 is Pending
        with self.assertRaises(ValueError):
            self.project.complete_project() # Should fail as phase1 is not completed

    @patch('core.models.project.send_mail') # Adjust path to where send_mail is imported in your model
    def test_complete_project_sends_notification(self, mock_send_mail):
        # Make all phases completable and complete them
        self.phase1.service_provider = self.consultant_user
        self.phase1.save()
        self.project.start_project(initial_phase=self.phase1)
        self.project.complete_phase(self.phase1)

        self.phase2.service_provider = self.consultant_user
        self.phase2.save()
        self.project.advance_to_phase(self.phase2)
        self.project.complete_phase(self.phase2) # This should trigger project completion and notifications

        self.project.refresh_from_db()
        self.assertEqual(self.project.status, STATUS_COMPLETED)
        self.assertEqual(mock_send_mail.call_count, 2) # One for customer, one for primary SP
        
        # Example assertion for one of the calls
        args_customer, kwargs_customer = mock_send_mail.call_args_list[0]
        self.assertIn(f"Your Project '{self.project.title}' is Complete!", kwargs_customer['subject'])
        self.assertIn(self.customer_user.email, kwargs_customer['recipient_list'])

class QuotationModelMethodTests(APITestCase):
    def setUp(self):
        self.customer_user = create_user(username="cust_quote", email="cq@example.com", user_type="Customer")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)
        self.service_provider_user = create_user(username="sp_quote", email="spq@example.com", user_type="Consultant")
        self.project = Projects.objects.create(customer=self.customer_profile, title="Quote Project")
        self.quotation = Quotation.objects.create(
            project=self.project,
            service_provider=self.service_provider_user,
            type="Initial Design",
            amount=1000.00,
            details="Design services"
        )

    @patch('core.models.project.send_mail') # Adjust path
    def test_approve_quotation(self, mock_send_mail):
        self.assertEqual(self.quotation.status, STATUS_PENDING)
        self.quotation.approve(approving_user=self.customer_user)
        self.quotation.refresh_from_db()
        self.assertEqual(self.quotation.status, STATUS_ACCEPTED)
        self.assertIsNotNone(self.quotation.approved_at)
        mock_send_mail.assert_called_once()
        args, kwargs = mock_send_mail.call_args
        self.assertIn(f"Quotation Approved", kwargs['subject'])
        self.assertIn(self.service_provider_user.email, kwargs['recipient_list'])

    @patch('core.models.project.send_mail') # Adjust path
    def test_reject_quotation(self, mock_send_mail):
        self.quotation.reject(rejecting_user=self.customer_user, reason="Too expensive")
        self.quotation.refresh_from_db()
        self.assertEqual(self.quotation.status, STATUS_REJECTED) # Assuming STATUS_REJECTED is defined
        # self.assertEqual(self.quotation.rejection_reason, "Too expensive") # If you add this field
        mock_send_mail.assert_called_once()


# --- API/View Tests ---

class AuthViewTests(APITestCase):
    def test_register_api_view(self):
        url = reverse('core:knox_register') # Make sure URL name is correct in urls.py
        data = {
            "username": "newreguser",
            "email": "newreg@example.com",
            "password": "newpassword123",
            "user_type": "Customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "newreguser")
        self.assertTrue(CustomerProfile.objects.filter(user__username="newreguser").exists())

    def test_login_api_view(self):
        create_user(username="loginuser", password="loginpass123")
        url = reverse('core:knox_login') # Make sure URL name is correct
        data = {"username": "loginuser", "password": "loginpass123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("expiry", response.data)


class ProjectsViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient() # Use APIClient for making requests
        self.customer_user = create_user(username="proj_cust", email="pc@example.com", user_type="Customer")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)

        self.sp_user = create_user(username="proj_sp", email="psp@example.com", user_type="Consultant")

        # Create a project for testing GET, PUT, etc.
        self.project1 = Projects.objects.create(customer=self.customer_profile, title="Project One")
        Phase.objects.create(project=self.project1, title="P1 Phase 1", order=1, service_provider=self.sp_user)

    def test_list_projects_as_customer(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:project-list') # Default router name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Or more, depending on how DRF pagination is set up
        self.assertEqual(response.data[0]['title'], "Project One")

    def test_create_project_as_customer(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:project-list')
        data = {"title": "New Project by Customer", "description": "A test description."}
        # If land_detail or primary_service_provider are required by serializer, include their IDs.
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Projects.objects.count(), 2)
        new_project = Projects.objects.get(title="New Project by Customer")
        self.assertEqual(new_project.customer, self.customer_profile)

    def test_create_project_as_service_provider_fails(self):
        self.client.force_authenticate(user=self.sp_user)
        url = reverse('core:project-list')
        data = {"title": "SP Project Attempt"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # PermissionDenied

    def test_start_project_action(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:project-start', kwargs={'pk': self.project1.pk}) # 'project-start' from router
        response = self.client.post(url) # Assuming phase1 is the default
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.status, STATUS_IN_PROGRESS)


class QuotationViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = create_user(username="quot_cust", user_type="Customer")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)
        self.sp_user = create_user(username="quot_sp", user_type="Consultant")
        self.project = Projects.objects.create(customer=self.customer_profile, title="Quotation Project")
        self.quotation1 = Quotation.objects.create(project=self.project, service_provider=self.sp_user, amount=500, type="Design")

    def test_sp_creates_quotation(self):
        self.client.force_authenticate(user=self.sp_user)
        url = reverse('core:quotation-list') # Assumes 'quotation-list' is the name from router
        data = {
            "project": self.project.pk,
            "type": "Detailed Plan",
            "amount": "1200.50",
            "details": "Very detailed."
            # service_provider is set by perform_create
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quotation.objects.count(), 2)

    def test_customer_approves_quotation_action(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('core:quotation-approve', kwargs={'pk': self.quotation1.pk}) # 'quotation-approve' from router
        
        with patch('core.models.project.send_mail') as mock_send_mail: # Patching where send_mail is called
            response = self.client.post(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.quotation1.refresh_from_db()
            self.assertEqual(self.quotation1.status, STATUS_ACCEPTED)
            mock_send_mail.assert_called_once() # Check if email was "sent"

    def test_other_user_cannot_approve_quotation(self):
        other_customer = create_user(username="othercust", user_type="Customer")
        self.client.force_authenticate(user=other_customer)
        url = reverse('core:quotation-approve', kwargs={'pk': self.quotation1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Permission Denied


# --- Signal Tests (Example for one signal) ---
# You've already tested some signal effects in UserModelTests (profile creation)

class UserSubscriptionSignalTest(APITestCase):
    @patch('core.signals.send_mail') # Path to send_mail in your signals.py
    def test_subscription_email_on_create(self, mock_send_mail):
        user = create_user(username="subuser", email="sub@example.com")
        plan = SubscriptionPlan.objects.create(name="Basic Plan", price=10, user_type='1') # '1' for Customer

        UserSubscription.objects.create(user=user, plan=plan, is_active=True)

        mock_send_mail.assert_called_once()
        args, kwargs = mock_send_mail.call_args
        self.assertEqual(kwargs['subject'], 'Subscription Confirmation')
        self.assertIn(user.email, kwargs['recipient_list'])


# TODO:
# - Tests for Profile Update Views
# - Tests for PhaseViewSet (creation, listing, actions)
# - Tests for DrawingViewSet, RevisionViewSet, DocumentViewSet
# - More detailed tests for permissions on all views and actions
# - Tests for failure cases (e.g., trying to advance to a non-existent phase)
# - Tests for serializers directly (validation, data representation)
# - Tests for your `apply_sub_promo_code` utility and its view.
# - Tests for ReferralListView.
# - Test different user types interacting with endpoints.
# - Test edge cases for all model methods.
# - Test listing with filters if you implement them in `get_queryset`.