from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch # For mocking email sending
import itertools
import uuid

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
phone_id_counter = itertools.count(start=1)

# --- Test Utility Functions (Optional) ---
def create_user(username="testuser", password="testpassword123", email="test@example.com", user_type="Customer", phone=None, **extra_fields):
    if phone is None:
        unique_id = next(phone_id_counter)
        # Create a phone like +97150123456 (total 12 chars, 9 digits after prefix)
        # or +971551234567 (total 13 chars, 10 digits after prefix)
        # Max 7 digits for the suffix if prefix is +9715X
        phone_suffix = str(unique_id).zfill(7) # Make it 7 digits long, e.g., 0000001
        if len(phone_suffix) > 7: # Safety, should not happen with zfill(7) if unique_id is reasonable
            # Fallback or raise error, this scheme only supports up to 9,999,999 unique test phones
            # For more, you'd need a more complex generation strategy or different prefixes
            phone_suffix = phone_suffix[-7:] # Take last 7 digits
        
        phone = f"+97150{phone_suffix}" # Example: +971500000001 (13 chars, 10 digits after +) - THIS FITS!
                                    # Or +97150 + 6 digits -> +97150123456 (12 chars, 9 digits after +) - THIS FITS!
                                    # Let's go with 6 digits for the suffix for a total of 12 chars.
        phone_suffix_6_digit = str(unique_id).zfill(6)
        if len(phone_suffix_6_digit) > 6:
            phone_suffix_6_digit = phone_suffix_6_digit[-6:]
        phone = f"+97150{phone_suffix_6_digit}" # e.g. +97150000001 (12 chars)

    # Ensure email is also unique for subsequent calls if not overridden by extra_fields
    # This logic should be before User.objects.create_user if email has a unique constraint
    final_email = email
    if 'email' not in extra_fields:
        # Check if the default email + username combination is unique enough
        # If creating many "testuser"s, this needs to be more robust
        temp_email_username = username
        if User.objects.filter(email=final_email).exists() and username != "testuser": # Avoid changing for the very first "testuser"
            base_email_part, domain_part = final_email.split('@')
            final_email = f"{base_email_part}_{temp_email_username}_{str(uuid.uuid4())[:4]}@{domain_part}"
        elif User.objects.filter(email=final_email).exists() and username == "testuser": # Default username but email exists
            base_email_part, domain_part = final_email.split('@')
            final_email = f"{base_email_part}_{str(uuid.uuid4())[:4]}@{domain_part}"


    # print(f"--- Creating user (helper): {username}, Email: {final_email}, Phone: {phone}, Type: {user_type} ---")
    return User.objects.create_user(
        username=username,
        password=password,
        email=final_email, # Use the potentially modified unique email
        user_type=user_type,
        phone=phone,
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
        self.assertGreaterEqual(mock_send_mail.call_count, 1) # One for customer, one for primary SP
        
        customer_email_sent = False
        sp_email_sent = False
        for call_args_tuple in mock_send_mail.call_args_list:
            args, kwargs_call = call_args_tuple # Renamed to avoid clash with outer scope kwargs
            recipient_list = kwargs_call.get('recipient_list', [])
            subject = kwargs_call.get('subject', '')

            if self.customer_user.email in recipient_list:
                expected_customer_subject = f"Your Project '{self.project.title}' is Complete!"
                self.assertEqual(subject, expected_customer_subject)
                customer_email_sent = True
            
            if self.project.primary_service_provider and self.project.primary_service_provider.email in recipient_list:
                # Update this expected subject based on your model method for SP
                expected_sp_subject = f"Project '{self.project.title}' Marked as Complete" 
                self.assertEqual(subject, expected_sp_subject)
                sp_email_sent = True
        
        self.assertTrue(customer_email_sent, "Email to customer regarding project completion was not sent or subject mismatch.")
        if self.project.primary_service_provider: # Only assert SP email if SP exists
            self.assertTrue(sp_email_sent, "Email to service provider regarding project completion was not sent or subject mismatch.")

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
        test_api_phone = "+971509876543" # 13 characters, 10 digits after +, valid
        unique_api_email_tag = str(uuid.uuid4())[:8]
        test_api_email = f"newreg_api_{unique_api_email_tag}@example.com"
        expected_username = "newreguser_api"
        data = {
            "username": expected_username, # Use a unique username for this API test
            "email": test_api_email,
            "password": "newpassword123",
            "user_type": "Customer",
            "phone": test_api_phone # Use a known good, unique phone
        }
        response = self.client.post(url, data, format='json')
        print(f"DEBUG Response Content (test_register_api_view): {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertTrue(User.objects.filter(username=expected_username).exists())
        created_user = User.objects.get(username=expected_username)
        self.assertEqual(created_user.username, expected_username)
        self.assertTrue(CustomerProfile.objects.filter(user=created_user).exists())

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
        print(f"DEBUG Response Content (test_create_project_as_customer): {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Projects.objects.count(), 2)
        new_project = Projects.objects.get(title="New Project by Customer")
        self.assertEqual(new_project.customer, self.customer_profile)

    def test_create_project_as_service_provider_fails(self):
        self.client.force_authenticate(user=self.sp_user)
        url = reverse('core:project-list')
        data = {"title": "SP Project Attempt"}
        response = self.client.post(url, data, format='json')
        print(f"DEBUG Response Content (test_create_project_as_service_provider_fails): {response.content.decode()}")
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
        self.customer_user = create_user(username="quot_cust", user_type="Customer", email="qcust@example.com", phone="+971500000001")
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)
        self.sp_user = create_user(username="quot_sp", user_type="Consultant", email="qsp@example.com", phone="+971500000002")
        self.project = Projects.objects.create(customer=self.customer_profile, title="Quotation Project")
        self.test_phase = Phase.objects.create(project=self.project, title="Test Phase for Quote", order=1, service_provider=self.sp_user)
        self.quotation1 = Quotation.objects.create(project=self.project, phase = self.test_phase, service_provider=self.sp_user, amount=500, type="Design")

    def test_sp_creates_quotation(self):
        self.client.force_authenticate(user=self.sp_user)
        url = reverse('core:quotation-list') # Assumes 'quotation-list' is the name from router
        data = {
            "project": self.project.pk,
            "phase_id": self.test_phase.pk,
            "type": "Detailed Plan",
            "amount": "1200.50",
            "details": "Very detailed.",
            # service_provider is set by perform_create
        }
        response = self.client.post(url, data, format='json')
        print("SP Creates Quotation Response Content:", response.content.decode())
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
        other_customer = create_user(username="othercust", user_type="Customer", email="oc@example.com", phone="+971500000003")
        self.client.force_authenticate(user=other_customer)
        url = reverse('core:quotation-approve', kwargs={'pk': self.quotation1.pk})
        response = self.client.post(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]) # Permission Denied


# --- Signal Tests (Example for one signal) ---
# You've already tested some signal effects in UserModelTests (profile creation)

class UserSubscriptionSignalTest(APITestCase):
    @patch('core.signals.send_mail') # Path to send_mail in your signals.py
    def test_subscription_email_on_create(self, mock_send_mail):
        user = create_user(username="subuser", email="sub@example.com")
        plan = SubscriptionPlan.objects.create(name="Basic Plan", price=10, user_type='1') # '1' for Customer
        
        mock_send_mail.reset_mock()

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