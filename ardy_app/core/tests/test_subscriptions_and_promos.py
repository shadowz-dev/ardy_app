# core/tests/test_subscriptions_and_promos.py
from django.test import TestCase # Can use TestCase if not many API calls, or APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from unittest.mock import patch
from django.utils import timezone
from datetime import timedelta

from ..models.user import User, SubscriptionPlan, UserSubscription, SubPromoCode, Referral
from ..serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer, ReferralSerializer # Import relevant serializers
from ..utils import apply_sub_promo_code # Your utility function
# from .test_users_and_auth import create_test_user # Import helper if it's in a common place or redefine

# Re-define or import create_test_user if needed
# phone_id_counter_subs_promos = itertools.count(start=300)
# def create_test_user_for_subs(...): ...

class SubscriptionPlanListViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        SubscriptionPlan.objects.create(name="Basic", price="10.00", user_type='1', is_active=True) # '1' for Customer
        SubscriptionPlan.objects.create(name="Pro", price="50.00", user_type='2', is_active=True)   # '2' for SP
        SubscriptionPlan.objects.create(name="Old Plan", price="5.00", user_type='1', is_active=False)
        self.url = reverse('core:subscription-plans')

    def test_list_active_subscription_plans(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Only Basic and Pro
        self.assertTrue(any(p['name'] == "Basic" for p in response.data))
        self.assertTrue(any(p['name'] == "Pro" for p in response.data))

class SubscribeToPlanViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = create_test_user_for_workflow(username_prefix="sub_cust", user_type="Customer")
        self.sp_user = create_test_user_for_workflow(username_prefix="sub_sp", user_type="Consultant")
        self.customer_plan = SubscriptionPlan.objects.create(name="Customer Monthly", price="20.00", user_type='1')
        self.sp_plan = SubscriptionPlan.objects.create(name="SP Pro", price="100.00", user_type='2')
        self.url = reverse('core:subscribe')

    @patch('core.signals.send_mail') # Assuming UserSubscription creation triggers an email
    def test_customer_subscribes_to_customer_plan(self, mock_send_mail):
        self.client.force_authenticate(user=self.customer_user)
        data = {"plan": self.customer_plan.pk}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content.decode())
        self.assertTrue(UserSubscription.objects.filter(user=self.customer_user, plan=self.customer_plan, is_active=True).exists())
        mock_send_mail.assert_called_once() # Check for subscription confirmation email

    def test_customer_cannot_subscribe_to_sp_plan(self):
        self.client.force_authenticate(user=self.customer_user)
        data = {"plan": self.sp_plan.pk}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("service providers only", response.data[0].lower()) # Check error message

    # Add test for SP subscribing to SP plan
    # Add test for user trying to subscribe when already actively subscribed (should deactivate old one)

class ApplySubPromoCodeUtilTests(TestCase): # Direct utility test
    def setUp(self):
        self.user = User.objects.create_user(username="promo_util_user", user_type="Customer", phone="+971...", email="pu@example.com")
        self.promo = SubPromoCode.objects.create(
            code="SAVE20", discount_percentage="20.00", max_uses=1, uses=0,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1), is_active=True
        )

    def test_apply_valid_promo_util(self):
        discount = apply_sub_promo_code(self.user, "SAVE20")
        self.assertEqual(discount, 20.00)
        self.promo.refresh_from_db()
        self.assertEqual(self.promo.uses, 1)

    def test_apply_used_promo_util_fails(self):
        apply_sub_promo_code(self.user, "SAVE20") # First use
        with self.assertRaises(ValueError): # Expecting a ValueError from your util
            apply_sub_promo_code(self.user, "SAVE20") # Second use should fail

    # Add tests for expired, inactive, non-existent codes for the utility

class ApplySubPromoCodeViewTests(APITestCase):
    # ... (similar to util tests, but through the API endpoint) ...
    pass

class ReferralListViewTests(APITestCase):
    # ... (tests as outlined in the previous step, ensure user creation is robust) ...
    pass