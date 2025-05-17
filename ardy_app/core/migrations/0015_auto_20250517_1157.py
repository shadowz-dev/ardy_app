from django.db import migrations

def delete_referencing_drawings(apps, schema_editor):
    Drawing = apps.get_model('core', 'Drawing')
    ConsultantProfile = apps.get_model('core', 'ConsultantProfile')

    # Identify ConsultantProfile rows that will be affected
    affected_consultant_profiles = ConsultantProfile.objects.all()  # Or a more specific filter

    # Delete Drawing rows that reference those ConsultantProfile rows
    Drawing.objects.filter(consultant__in=affected_consultant_profiles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_companyprofile_employees'),  # Replace with the correct dependency
    ]

    operations = [
        migrations.RunPython(delete_referencing_drawings),
    ]