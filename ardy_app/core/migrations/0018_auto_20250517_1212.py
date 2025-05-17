from django.db import migrations

def delete_orphaned_drawings(apps, schema_editor):
    Drawing = apps.get_model('core', 'Drawing')
    ConsultantProfile = apps.get_model('core', 'ConsultantProfile')

    # Find Drawing records where the related ConsultantProfile does not exist.
    orphaned_drawings = Drawing.objects.filter(consultant__isnull=True)

    # Delete the orphaned Drawing records.
    orphaned_drawings.delete()


def reverse_delete_orphaned_drawings(apps, schema_editor):
    # This is tricky to reverse, as we'd need to know *how* to recreate the
    # ConsultantProfile relationships.  For safety, we'll just leave it blank.
    pass  # Or raise an exception to indicate that reversal is not possible.


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20250517_1200'),  # Replace with the migration that introduces BaseProfile
    ]

    operations = [
        migrations.RunPython(delete_orphaned_drawings, reverse_code=reverse_delete_orphaned_drawings),
    ]