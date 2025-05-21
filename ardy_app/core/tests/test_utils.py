# core/tests/test_utils.py
from django.test import TestCase
from ..utils import apply_sub_promo_code # Adjust import
from ..models import User, SubPromoCode # Adjust
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class PromoCodeUtilTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="promo_user",)
        self.valid_promo = SubPromoCode.objects.create(
            code="SAVE10", discount_percentage=10, max_uses=5, uses=0,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1), is_active=True
        )
        self.expired_promo = SubPromoCode.objects.create(code="EXPIRED", ) # Make it expired

    def test_apply_valid_promo_code(self):
        discount = apply_sub_promo_code(self.user, "SAVE10")
        self.assertEqual(discount, 10)
        self.valid_promo.refresh_from_db()
        self.assertEqual(self.valid_promo.uses, 1)

    def test_apply_invalid_code(self):
        with self.assertRaises(ValueError): # Or your custom exception
            apply_sub_promo_code(self.user, "INVALIDCODE")

    # Test for expired, max_uses reached, inactive promos
    
class ApplyPromoCodeViewTests(APITestCase):
    # setUp with user, valid promo code
    def test_apply_valid_promo_view(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('core:apply-promo')
        response = self.client.post(url, {"promo_code": "SAVE10"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['discount_percent'], 10)
    # Test for invalid code, already used, etc.