# core/tests/test_profile_views.py (or in your main tests.py)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..tests import create_user # Assuming create_user is in a common setup file or tests.py
from ..models.user import CustomerProfile, User # Adjust import

class CustomerProfileUpdateViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(username="cust_profile_test", user_type="Customer", email="cpt@example.com", phone="+971501112233")
        # Profile should be created by signal, let's ensure it exists
        self.profile, _ = CustomerProfile.objects.get_or_create(user=self.user, defaults={'budget': 1000})
        self.url = reverse('core:customer-profile-detail') # Assuming this is the URL name

    def test_retrieve_own_customer_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.data['budget'], 1000)

    def test_update_own_customer_profile(self):
        self.client.force_authenticate(user=self.user)
        update_data = {
            "budget": 5000,
            "property_status": "Actively Looking",
            "project_details": "Looking for a 3-bedroom villa."
            # 'user' field should not be updatable here by the client; view's get_object handles it
        }
        response = self.client.put(self.url, update_data, format='json') # Or PATCH for partial update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.budget, 5000)
        self.assertEqual(self.profile.property_status, "Actively Looking")

    def test_unauthenticated_user_cannot_access_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Or 403 if IsAuthenticated is default

    def test_other_user_type_cannot_access_customer_profile(self):
        other_user = create_user(username="consultant_tries", user_type="Consultant", email="ct@example.com", phone="+971504445566")
        self.client.force_authenticate(user=other_user)
        response = self.client.get(self.url)
        # Expect 403 because IsCustomer permission should fail, after IsAuthenticated passes
        # Or 404 if get_object in UserProfileView raises DoesNotExist/PermissionDenied for wrong type
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

# Similar test classes for ConsultantProfileUpdateView, InteriorProfileUpdateView, etc.