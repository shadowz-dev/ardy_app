# Generated by Django 3.2.25 on 2025-05-26 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='constructionprofile',
            old_name='service_offered',
            new_name='services_offered',
        ),
        migrations.RenameField(
            model_name='consultantprofile',
            old_name='service_offered',
            new_name='services_offered',
        ),
        migrations.RenameField(
            model_name='interiorprofile',
            old_name='service_offered',
            new_name='services_offered',
        ),
        migrations.RenameField(
            model_name='maintenanceprofile',
            old_name='service_offered',
            new_name='services_offered',
        ),
        migrations.RenameField(
            model_name='smarthomeprofile',
            old_name='service_offered',
            new_name='services_offered',
        ),
        migrations.AddField(
            model_name='subscriptionplan',
            name='is_default_free_plan',
            field=models.BooleanField(default=False, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='constructionprofile',
            name='experience',
            field=models.IntegerField(blank=True, help_text='Years of experience', null=True),
        ),
        migrations.AlterField(
            model_name='consultantprofile',
            name='experience',
            field=models.IntegerField(blank=True, help_text='Years of experience', null=True),
        ),
        migrations.AlterField(
            model_name='interiorprofile',
            name='experience',
            field=models.IntegerField(blank=True, help_text='Years of experience', null=True),
        ),
        migrations.AlterField(
            model_name='maintenanceprofile',
            name='experience',
            field=models.IntegerField(blank=True, help_text='Years of experience', null=True),
        ),
        migrations.AlterField(
            model_name='smarthomeprofile',
            name='experience',
            field=models.IntegerField(blank=True, help_text='Years of experience', null=True),
        ),
        migrations.AlterField(
            model_name='usersubscription',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.subscriptionplan'),
        ),
    ]
