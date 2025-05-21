from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import uuid
from .constants import (STATUS_ACCEPTED,STATUS_CANCELLED,STATUS_COMPLETED,STATUS_IN_PROGRESS,STATUS_PENDING,STATUS_REJECTED, SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL)

from .models.user import User, CustomerProfile, ConsultantProfile, ConstructionProfile, InteriorProfile, MaintenanceProfile, SmartHomeProfile, UserSubscription
from .models.project import Phase, Quotation,Drawing,Revision,Document,Projects
from .models import Referral

@receiver(post_save, sender=Quotation)
def notify_customer_on_quotation(sender, instance, created, **kwargs): # Renamed for clarity
    if created:
        try:
            customer_email = instance.project.customer.user.email
            phase_info = f" for phase '{instance.phase.title}'" if instance.phase else ""
            message_body = (
                f"Dear {instance.project.customer.user.first_name or instance.project.customer.user.username},\n\n"
                f"A new quotation of type '{instance.type}' has been provided by service provider "
                f"'{instance.service_provider.username}' for your project '{instance.project.title}'{phase_info}.\n\n"
                f"Quotation Amount: {instance.amount}\n"
                f"Details: {instance.details}\n\n"
                f"You can view it in the Ardy-App."
            )
            send_mail(
                subject=f"New Quotation for Project: {instance.project.title}",
                message=message_body,
                from_email=settings.DEFAULT_FROM_EMAIL, # Use settings
                recipient_list=[customer_email],
                fail_silently=False, # Or True in production if email failure shouldn't break the request
            )
        except AttributeError as e:
            # Catch cases where related objects might not exist yet or are None
            print(f"Error sending quotation notification for Quotation ID {instance.id}: {e}")
        except Exception as e: # Catch other potential errors during email sending
            print(f"General error sending quotation notification for Quotation ID {instance.id}: {e}")

@receiver(post_save, sender=Drawing)
def notify_customer_on_drawing_upload(sender, instance, created, **kwargs): # Renamed
    if created:
        try:
            customer_email = instance.project.customer.user.email
            uploader_name = "N/A"
            if instance.uploaded_by:
                uploader_name = instance.uploaded_by.username
            # elif instance.uploaded_by_consultant: # If you use this field primarily
            # uploader_name = instance.uploaded_by_consultant.user.username

            phase_info = f" for phase '{instance.phase.title}'" if instance.phase else ""
            message_body = (
                f"Dear {instance.project.customer.user.first_name or instance.project.customer.user.username},\n\n"
                f"A new drawing (Title: '{instance.title}', Version: {instance.version}) has been uploaded by "
                f"'{uploader_name}' for your project '{instance.project.title}'{phase_info}.\n\n"
                f"Notes: {instance.notes or 'N/A'}\n\n"
                f"You can view it in the Ardy-App."
            )
            send_mail(
                subject=f"New Drawing Uploaded for Project: {instance.project.title}",
                message=message_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_email],
                fail_silently=False,
            )
        except AttributeError as e:
            print(f"Error sending drawing upload notification for Drawing ID {instance.id}: {e}")
        except Exception as e:
            print(f"General error sending drawing upload notification for Drawing ID {instance.id}: {e}")
        
@receiver(post_save, sender=Revision)
def notify_uploader_on_revision_request(sender, instance, created, **kwargs): # Renamed
    if created:
        try:
            target_user = None
            if instance.drawing.uploaded_by:
                target_user = instance.drawing.uploaded_by
            # elif instance.drawing.uploaded_by_consultant:
                # target_user = instance.drawing.uploaded_by_consultant.user

            if target_user and target_user.email:
                message_body = (
                    f"Dear {target_user.first_name or target_user.username},\n\n"
                    f"A new revision has been requested by customer "
                    f"'{instance.customer.user.username}' for your drawing "
                    f"'{instance.drawing.title}' (Version: {instance.drawing.version}) "
                    f"on project '{instance.drawing.project.title}'.\n\n"
                    f"Comment: {instance.comment}\n\n"
                    f"Please review it in the Ardy-App."
                )
                send_mail(
                    subject=f"Revision Requested for Drawing: {instance.drawing.title}",
                    message=message_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[target_user.email],
                    fail_silently=False,
                )
            else:
                print(f"Could not determine recipient for revision request on Drawing ID {instance.drawing.id}")
        except AttributeError as e:
            print(f"Error sending revision request notification for Revision ID {instance.id}: {e}")
        except Exception as e:
            print(f"General error sending revision request notification for Revision ID {instance.id}: {e}")

@receiver(post_save, sender=UserSubscription)
def send_subscription_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Subscription Confirmation',
            message=f"Thank you for subscribing to {instance.plan.name}! Your subscription has been confirmed.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
        )

# --- Consolidated User Post-Save Actions ---
@receiver(post_save, sender=User)
def handle_new_user_created(sender, instance, created, **kwargs):
    if created:
        #print(f"[Signal] New user created: {instance.username}, Type: {instance.user_type}")

        # 1. Create Referral Code
        try:
            referral, ref_created = Referral.objects.get_or_create(
                referrer=instance,
                defaults={'code': f"REF-{str(uuid.uuid4()).upper().replace('-', '')[:10]}"}
            )
            #print(f"[Signal] Referral for {instance.username} {'created' if ref_created else 'retrieved'}: {referral.code}")
        except Exception as e:
            print(f"[Signal Error] Creating referral for {instance.username}: {e}")

        # 2. Send Welcome Email
        try:
            send_mail(
                subject='Welcome to Ardy-App!',
                message=f"Hi {instance.first_name or instance.username},\n\nWelcome to Ardy-App! We're excited to have you.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False, # Good for dev, consider True for prod with logging
            )
            #print(f"[Signal] Welcome email sent to {instance.email}")
        except Exception as e:
            print(f"[Signal Error] Sending welcome email to {instance.email}: {e}")

        # 3. Auto-create Profile based on user_type
        user_type_str = instance.user_type
        #print(f"[Signal] Attempting to create profile for type: {user_type_str}")
        profile_created_successfully = False
        try:
            if user_type_str == 'Customer':
                profile, p_created = CustomerProfile.objects.get_or_create(user=instance)
                if p_created: #print(f"[Signal] CustomerProfile created for {instance.username}")
                    profile_created_successfully = True
            elif user_type_str == 'Consultant':
                profile, p_created = ConsultantProfile.objects.get_or_create(user=instance)
                if p_created: #print(f"[Signal] ConsultantProfile created for {instance.username}")
                    profile_created_successfully = True
            elif user_type_str == 'Interior Designer':
                profile, p_created = InteriorProfile.objects.get_or_create(user=instance)
                if p_created: #print(f"[Signal] InteriorProfile created for {instance.username}")
                    profile_created_successfully = True
            elif user_type_str == 'Construction':
                profile, p_created = ConstructionProfile.objects.get_or_create(user=instance)
                if p_created: #print(f"[Signal] ConstructionProfile created for {instance.username}")
                    profile_created_successfully = True
            elif user_type_str == 'Maintenance': # Check spelling consistency
                profile, p_created = MaintenanceProfile.objects.get_or_create(user=instance) # Check spelling
                if p_created: #print(f"[Signal] MaintenanceProfile created for {instance.username}")
                    profile_created_successfully = True
            elif user_type_str == 'Smart_Home': # Check 'Smart_Home' vs 'Smart Home' from constants
                profile, p_created = SmartHomeProfile.objects.get_or_create(user=instance)
                if p_created: #print(f"[Signal] SmartHomeProfile created for {instance.username}")
                    profile_created_successfully = True
            else:
                print(f"[Signal Warning] Unknown user_type '{user_type_str}' for profile creation for user {instance.username}.")

            if not profile_created_successfully and user_type_str not in ['Admin']: # Assuming Admins might not need these profiles
                print(f"[Signal Error] Profile NOT created for {instance.username} of type {user_type_str} but was expected.")

        except Exception as e:
            print(f"[Signal Error] Creating profile for {instance.username} of type {user_type_str}: {e}")

        # 4. Notify admin if it's a service provider type needing approval
        if user_type_str in SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL:
            try:
                admin_emails = User.objects.filter(user_type='Admin', is_staff=True, is_active=True).values_list('email', flat=True)
                if admin_emails:
                    send_mail(
                        subject='New Service Provider Registration for Approval',
                        message=f"User {instance.username} ({instance.email}) has registered as a {instance.get_user_type_display()} and may need approval.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=list(admin_emails),
                        fail_silently=False,
                    )
                    print(f"[Signal] Admin notification sent for new SP: {instance.username}")
                else:
                    pass#print(f"[Signal Warning] No active admin users found to notify for new SP: {instance.username}")
            except Exception as e:
                print(f"[Signal Error] Notifying admin for new SP {instance.username}: {e}")

# REMOVE the other two User post_save handlers:
# - create_referral_code (its logic is now in handle_new_user_created)
# - user_post_save_actions (this was incomplete/redundant)
# - create_user_profile_and_send_welcome (its logic is now in handle_new_user_created)