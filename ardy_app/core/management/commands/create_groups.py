from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import User

class Command(BaseCommand):
    help = 'Create default user groups and permissions'

    def handle(self, *args, **kwargs):
        groups = {
            'Customers': [],
            'Consultants': ['can_submit_quotation', 'can_upload_drawings'],
            'Construction': ['can_submit_quotation','can_update_project_phases'],
            'InteriorDesigners': ['can_submit_quotation','can_upload_designes'],
            'Admins': ['can_approve_users', 'can_manage_projects'],
        }

        for group_name, permissions in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_codename in permissions:
                permission, _ = Permission.objects.get_or_create(
                    name=f"Can {perm_codename.replace('-', ' ')}",
                    content_type=ContentType.objects.get_for_model(User),
                )
                group.permissions.add(permission)
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' updated"))
        self.stdout.write(self.style.SUCCESS("Groups and permissions set up"))
