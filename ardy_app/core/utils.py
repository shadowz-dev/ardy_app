from .models import SubPromoCode, Referral
from django.utils.timezone import now

def apply_sub_promo_code(user, promo_code):
        try:
            promo = SubPromoCode.objects.get(code=promo_code)
            if promo.is_valid():
                promo.uses += 1
                promo.save()
                return promo.discount_percent
            else:
                raise ValueError("Promo code is invalid or expired.")
        except SubPromoCode.DoesNotExist:
            raise ValueError("Promo code does not exist.")
        
def reward_referrer(user):
    try:
        referral = Referral.objects.get(referred_user=user, is_redeemed=False)
        referrer = referral.referrer

        # Add reward to referrer (e.g., credit or discount)
        referral.reward += 10.00  # Example reward amount
        referral.is_redeemed = True
        referral.save()
    except Referral.DoesNotExist:
        pass