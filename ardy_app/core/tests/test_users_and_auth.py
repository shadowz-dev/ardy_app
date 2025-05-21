# core/tests/test_users_and_auth.py

import uuid
import itertools
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch

# Adjust these imports based on your exact model locations
from ..models import (
    User as UserModel, # Alias to avoid clash if needed
    CustomerProfile,
    ConsultantProfile,
    InteriorProfile,
    ConstructionProfile,
    MaintenanceProfile,
    SmartHomeProfile,
    Referral
)
# If USER_TYPES and SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL are in constants
from ..constants import USER_TYPES, SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL


User = get_user_model()

# --- Test Utility Functions ---
# Global counter for unique phone numbers in tests
phone_id_counter_users_auth = itertools.count(start=1)

def create_test_user(username_prefix="testuser", email_prefix="test", user_type="Customer", password="testpassword123", make_unique=True, **extra_fields):
    """
    Creates a user with potentially unique username, email, and phone.
    """
    unique_suffix = ""
    if make_unique:
        unique_suffix = f"_{uuid.uuid4().hex[:6]}"

    username = f"{username_prefix}{unique_suffix}"
    email = f"{email_prefix}{unique_suffix}@example.com"
    
    phone = extra_fields.pop('phone', None)
    if phone is None:
        # Generate unique phone based on counter
        unique_id = next(phone_id_counter_users_auth)
        phone_suffix_6_digit = str(unique_id).zfill(6)
        if len(phone_suffix_6_digit) > 6: # Safety for very many tests
            phone_suffix_6_digit = phone_suffix_6_digit[-6:]
        phone = f"+97150{phone_suffix_6_digit}"

    # print(f"--- Creating user (helper): {username}, Email: {email}, Phone: {phone}, Type: {user_type} ---")
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        user_type=user_type,
        phone=phone,
        **extra_fields
    )

# --- Model & Signal Tests ---
class UserModelAndSignalTests(APITestCase):
    def test_create_user_successfully(self):
        user = create_test_user(username_prefix="simple_user", user_type="Consultant")
        self.assertEqual(user.user_type, "Consultant")
        self.assertTrue(user.check_password("testpassword123"))

    @patch('core.signals.send_mail') # Patch where send_mail is called in your signal
    def test_user_creation_signals_customer(self, mock_send_mail):
        user = create_test_user(username_prefix="cust_signal", user_type="Customer")

        # 1. Test Profile Creation
        self.assertTrue(CustomerProfile.objects.filter(user=user).exists(), "CustomerProfile not created.")
        
        # 2. Test Referral Code Creation
        self.assertTrue(Referral.objects.filter(referrer=user).exists(), "Referral code not created.")
        referral = Referral.objects.get(referrer=user)
        self.assertTrue(referral.code.startswith("REF-"), "Referral code format incorrect.")

        # 3. Test Welcome Email
        welcome_email_sent = False
        admin_notification_sent = False
        for call_args_tuple in mock_send_mail.call_args_list:
            _, kwargs = call_args_tuple
            if kwargs.get('subject') == 'Welcome to Ardy-App!':
                self.assertIn(user.email, kwargs['recipient_list'])
                welcome_email_sent = True
            if kwargs.get('subject') == 'New Service Provider Registration for Approval':
                admin_notification_sent = True # Should not be sent for customer

        self.assertTrue(welcome_email_sent, "Welcome email not sent.")
        self.assertFalse(admin_notification_sent, "Admin notification sent for Customer, but should not have been.")

    @patch('core.signals.send_mail')
    def test_user_creation_signals_service_provider(self, mock_send_mail):
        # Ensure SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL is defined and imported
        # For this test, pick one type that IS in SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL
        sp_type_to_test = "Consultant" # Assuming this is in the approval list
        if sp_type_to_test not in [ut[0] for ut in USER_TYPES if ut[0] in SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL]:
            self.skipTest(f"{sp_type_to_test} not configured for admin approval notification, skipping part of test.")
            return


        # Create an admin user to receive notifications
        admin_user = create_test_user(username_prefix="admin_for_notify", user_type="Admin", is_staff=True, make_unique=False) # Fixed admin for predictable email

        user_sp = create_test_user(username_prefix="sp_signal", user_type=sp_type_to_test)

        # 1. Test Profile Creation (e.g., ConsultantProfile)
        self.assertTrue(ConsultantProfile.objects.filter(user=user_sp).exists(), f"{sp_type_to_test}Profile not created.")

        # 2. Test Admin Notification for SP
        admin_notification_sent = False
        for call_args_tuple in mock_send_mail.call_args_list:
            _, kwargs = call_args_tuple
            if kwargs.get('subject') == 'New Service Provider Registration for Approval':
                self.assertIn(admin_user.email, kwargs['recipient_list']) # Check if admin was notified
                admin_notification_sent = True
                break
        
        # Only assert if there's an admin to notify
        if User.objects.filter(user_type='Admin', is_staff=True, is_active=True).exists():
            self.assertTrue(admin_notification_sent, "Admin notification for new SP not sent.")
        else:
            print("[Test Warning] No active admin user found in DB, skipping admin notification check.")


# --- Authentication API View Tests ---
class AuthViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # A user for login tests
        self.login_user_username = "loginuser_auth"
        self.login_user_email = "login_auth@example.com"
        self.login_user_phone = "+971509998877"
        self.login_user_password = "loginpassword123"
        create_test_user(
            username_prefix=self.login_user_username, # Pass the exact username
            email_prefix="login_auth_email", # Pass a prefix, helper will make it unique
            phone=self.login_user_phone,
            password=self.login_user_password,
            user_type="Customer",
            make_unique=False # Ensure predictable username for login
        )

    def test_register_api_view_customer(self):
        url = reverse('core:knox_register') # Ensure this URL name is correct
        
        reg_username = "new_reg_cust"
        reg_email_prefix = "newregcust"
        reg_phone = "+971501234500" # Unique for this test

        data = {
            "username": reg_username,
            "email": f"{reg_email_prefix}_{uuid.uuid4().hex[:4]}@example.com", # Ensure unique email
            "password": "newpassword123",
            "user_type": "Customer", # Valid choice from USER_TYPES
            "phone": reg_phone
        }
        response = self.client.post(url, data, format='json')
        # print(f"DEBUG Response Content (test_register_api_view_customer): {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content.decode())
        self.assertIn("token", response.data)
        self.assertEqual(response.data['user']['username'], reg_username)
        self.assertTrue(User.objects.filter(username=reg_username).exists())
        self.assertTrue(CustomerProfile.objects.filter(user__username=reg_username).exists())

    def test_register_api_view_missing_phone(self):
        url = reverse('core:knox_register')
        data = {"username": "nophoneuser", "email": "np@example.com", "password": "password", "user_type": "Customer"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data) # Expecting error message for phone

    def test_login_api_view_success(self):
        url = reverse('core:knox_login') # Ensure this URL name is correct
        data = {"username": self.login_user_username, "password": self.login_user_password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.assertIn("token", response.data)
        self.assertIn("expiry", response.data)

    def test_login_api_view_failure_wrong_password(self):
        url = reverse('core:knox_login')
        data = {"username": self.login_user_username, "password": "wrongpassword"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # Knox login might return 400 for bad creds
        self.assertNotIn("token", response.data)

    def test_logout_view(self):
        # First, login to get a token
        login_url = reverse('core:knox_login')
        login_data = {"username": self.login_user_username, "password": self.login_user_password}
        login_response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['token']

        # Now, logout using the token
        logout_url = reverse('core:knox_logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') # Set token for logout request
        response = self.client.post(logout_url) # Knox logout is a POST
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# --- Profile Detail View Tests (Retrieve & Update) ---
class CustomerProfileDetailViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_test_user(username_prefix="profile_cust", user_type="Customer")
        self.profile, created = CustomerProfile.objects.get_or_create(user=self.user, defaults={'budget': 100}) # Signal should have created this
        if created or self.profile.budget != 1000: # Only update if newly created or different
            self.profile.budget = 1000
            self.profile.property_status = "Initial Test Status" # Add other fields
            self.profile.save()
        self.url = reverse('core:customer-profile-detail') # Assumes URL name

    def test_authenticated_customer_can_retrieve_own_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.user.pk)
        self.assertEqual(response.data['budget'], 1000)

    def test_authenticated_customer_can_update_own_profile(self):
        self.client.force_authenticate(user=self.user)
        update_data = {"budget": 12345, "property_status": "Updated Status"}
        response = self.client.put(self.url, update_data, format='json') # PUT for full update
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.budget, 12345)
        self.assertEqual(self.profile.property_status, "Updated Status")

    def test_unauthenticated_cannot_retrieve_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Or 403 if IsAuthenticated is default

    def test_consultant_cannot_retrieve_customer_profile_via_this_endpoint(self):
        consultant_user = create_test_user(username_prefix="consultant_profile_viewer", user_type="Consultant")
        self.client.force_authenticate(user=consultant_user)
        response = self.client.get(self.url)
        # Expect 403 (Permission Denied by IsCustomer) or 404 (if get_object filters and finds nothing)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

# --- Consultant Profile Detail View Tests ---
class ConsultantProfileDetailViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.consultant_user = create_test_user(username_prefix="profile_consultant", user_type="Consultant")
        # Profile should be created by signal
        self.profile, created = ConsultantProfile.objects.get_or_create(
            user=self.consultant_user,
            defaults={}
        )
        self.profile.company_name = "Initial Consult Co"
        self.profile.expertise = "Structural Engineering"
        self.profile.save()
        self.url = reverse('core:consultant-profile-detail') # Assumes this URL name

    def test_authenticated_consultant_can_retrieve_own_profile(self):
        self.client.force_authenticate(user=self.consultant_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.consultant_user.pk)
        self.assertEqual(response.data['company_name'], "Initial Consult Co")

    def test_authenticated_consultant_can_update_own_profile(self):
        self.client.force_authenticate(user=self.consultant_user)
        update_data = {
            "company_name": "Updated Consult Co",
            "expertise": "Structural Engineering",
            "experience": 5,
            "portfolio": "http://myportfolio.example.com",
            "introduction": "Experienced structural engineer.",
            "projects_completed": 20
            # 'company_profile' (FileField) would require different handling for upload if tested here
        }
        response = self.client.put(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.company_name, "Updated Consult Co")
        self.assertEqual(self.profile.expertise, "Structural Engineering")
        self.assertEqual(self.profile.experience, 5)

    def test_unauthenticated_cannot_retrieve_consultant_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_cannot_retrieve_consultant_profile_via_this_endpoint(self):
        customer_user = create_test_user(username_prefix="customer_profile_viewer", user_type="Customer")
        self.client.force_authenticate(user=customer_user)
        response = self.client.get(self.url)
        # Expect 403 (Permission Denied by IsConsultant) or 404 (if get_object filters and finds nothing)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_update_consultant_profile_with_invalid_data(self):
        self.client.force_authenticate(user=self.consultant_user)
        invalid_data = {"experience": "not_an_integer"} # experience is an IntegerField
        response = self.client.put(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('experience', response.data)


# --- Interior Designer Profile Detail View Tests ---
class InteriorProfileDetailViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.interior_user = create_test_user(username_prefix="profile_interior", user_type="Interior Designer")
        # Profile should be created by signal
        self.profile, created = InteriorProfile.objects.get_or_create(
            user=self.interior_user,
            defaults={}
        )
        self.profile.company_name = "Chic Designs"
        self.profile.expertise = "Residential & Commercial"
        self.profile.save()
        self.url = reverse('core:interior-profile-detail') # Assumes this URL name

    def test_authenticated_interior_can_retrieve_own_profile(self):
        self.client.force_authenticate(user=self.interior_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.interior_user.pk)
        self.assertEqual(response.data['company_name'], "Chic Designs")

    def test_authenticated_interior_can_update_own_profile(self):
        self.client.force_authenticate(user=self.interior_user)
        update_data = {
            "company_name": "Luxury Interiors Inc.",
            "expertise": "Residential & Commercial",
            "experience": 10,
            # Add other relevant fields for InteriorProfile
        }
        response = self.client.put(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.company_name, "Luxury Interiors Inc.")
        self.assertEqual(self.profile.experience, 10)

    def test_unauthenticated_cannot_retrieve_interior_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_consultant_cannot_retrieve_interior_profile_via_this_endpoint(self):
        consultant_user = create_test_user(username_prefix="consultant_profile_viewer2", user_type="Consultant")
        self.client.force_authenticate(user=consultant_user)
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
        
# --- Construction Profile Detail View Tests ---
class ConstructionProfileDetailViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.construction_user = create_test_user(username_prefix="profile_construct", user_type="Construction")
        # Profile should be created by signal
        self.profile, crated = ConstructionProfile.objects.get_or_create(
            user=self.construction_user,
            defaults={}
        )
        self.profile.company_name = "BuildIt Right"
        self.profile.expertise = "Residential and Commercial Construction"
        self.profile.experience = 2
        self.profile.projects_completed = 1
        self.profile.save()
        self.url = reverse('core:construction-profile-detail') # Assumes this URL name

    def test_authenticated_construction_can_retrieve_own_profile(self):
        self.client.force_authenticate(user=self.construction_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.construction_user.pk)
        self.assertEqual(response.data['company_name'], "BuildIt Right")

    def test_authenticated_construction_can_update_own_profile(self):
        self.client.force_authenticate(user=self.construction_user)
        update_data = {
            "company_name": "Solid Foundations Ltd.",
            "expertise": "Commercial and Residential Construction",
            "experience": 15,
            "projects_completed": 50
        }
        response = self.client.put(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.company_name, "Solid Foundations Ltd.")
        self.assertEqual(self.profile.experience, 15)

    def test_unauthenticated_cannot_retrieve_construction_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_cannot_retrieve_construction_profile_via_this_endpoint(self):
        customer_user = create_test_user(username_prefix="customer_construct_viewer", user_type="Customer")
        self.client.force_authenticate(user=customer_user)
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])


# --- Maintenance Profile Detail View Tests ---
# Assuming your model is MaintenanceProfile and user_type is 'Maintenance'
class MaintenanceProfileDetailViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Ensure 'Maintenance' is a valid choice in your USER_TYPES
        # and MaintenanceProfile model exists
        self.maintenance_user = create_test_user(username_prefix="profile_maint", user_type="Maintenance")
        self.profile, _ = MaintenanceProfile.objects.get_or_create(
            user=self.maintenance_user,
            defaults={}
        )
        self.profile.company_name = "FixIt Quick"
        self.profile.expertise = "Home Maintenance"
        self.profile.experience = 2
        self.profile.projects_completed = 1
        self.profile.save()
        self.url = reverse('core:maintenance-profile-detail') # Assumes this URL name

    def test_authenticated_maintenance_can_retrieve_own_profile(self):
        self.client.force_authenticate(user=self.maintenance_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.maintenance_user.pk)
        self.assertEqual(response.data['company_name'], "FixIt Quick")

    def test_authenticated_maintenance_can_update_own_profile(self):
        self.client.force_authenticate(user=self.maintenance_user)
        update_data = {
            "company_name": "Reliable Repairs Co.",
            "expertise": "General Home Maintenance",
            "experience": 8,
            "projects_completed": 100 # Assuming 'projects_completed' is the field name
        }
        response = self.client.put(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.company_name, "Reliable Repairs Co.")
        self.assertEqual(self.profile.experience, 8)

    def test_unauthenticated_cannot_retrieve_maintenance_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_consultant_cannot_retrieve_maintenance_profile_via_this_endpoint(self):
        consultant_user = create_test_user(username_prefix="consultant_maint_viewer", user_type="Consultant")
        self.client.force_authenticate(user=consultant_user)
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])


# --- SmartHome Profile Detail View Tests ---
# Assuming your model is SmartHomeProfile and user_type is 'Smart_Home' or 'Smart Home'
class SmartHomeProfileDetailViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Ensure 'Smart_Home' (or 'Smart Home') is a valid choice in USER_TYPES
        # and SmartHomeProfile model exists
        self.smarthome_user = create_test_user(username_prefix="profile_smarthome", user_type="Smart_Home")
        self.profile, created = SmartHomeProfile.objects.get_or_create(
            user=self.smarthome_user,
            defaults={}
        )
        self.profile.company_name = "Future Living Tech"
        self.profile.expertise = "Smart Home Automation"
        self.profile.experience = 3
        self.profile.projects_completed = 5
        self.profile.save()
        self.url = reverse('core:smarthome-profile-detail') # Assumes this URL name

    def test_authenticated_smarthome_can_retrieve_own_profile(self):
        self.client.force_authenticate(user=self.smarthome_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.smarthome_user.pk)
        self.assertEqual(response.data['company_name'], "Future Living Tech")

    def test_authenticated_smarthome_can_update_own_profile(self):
        self.client.force_authenticate(user=self.smarthome_user)
        update_data = {
            "company_name": "IntelliHome Solutions",
            "expertise": "Full Home Automation & IoT",
            "experience": 7,
            "projects_completed": 30
        }
        response = self.client.put(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content.decode())
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.company_name, "IntelliHome Solutions")
        self.assertEqual(self.profile.experience, 7)

    def test_unauthenticated_cannot_retrieve_smarthome_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_cannot_retrieve_smarthome_profile_via_this_endpoint(self):
        customer_user = create_test_user(username_prefix="customer_smarthome_viewer", user_type="Customer")
        self.client.force_authenticate(user=customer_user)
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
