from django.db import migrations
from django.db import connection


def enable_foreign_key_constraints(apps, schema_editor):
    if schema_editor.connection.vendor == 'sqlite':
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys = ON;")


def reverse_enable_foreign_key_constraints(apps, schema_editor):
    if schema_editor.connection.vendor == 'sqlite':
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys = OFF;")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20250517_1157'),  # Replace with the correct dependency
    ]

    operations = [
        migrations.RunPython(enable_foreign_key_constraints, reverse_code=reverse_enable_foreign_key_constraints),
    ]