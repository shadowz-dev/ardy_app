# Generated by Django 3.2.25 on 2024-11-23 06:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_subscriptionplan_usersubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed.", regex='^\\+?1?\\d{9,14}$')])),
                ('password', models.CharField(default=0, max_length=50)),
                ('otp', models.CharField(blank=True, max_length=9, null=True)),
                ('count', models.IntegerField(default=0, help_text='Number of otp sent')),
                ('logged', models.BooleanField(default=False, help_text='If otp verification got successful')),
                ('forgot', models.BooleanField(default=False, help_text='only true for forgot password')),
                ('forgot_logged', models.BooleanField(default=False, help_text='Only true if validate otp forgot get successful')),
                ('referral_code', models.CharField(blank=True, max_length=200, null=True)),
                ('signup_type', models.CharField(choices=[('Manual', 'Manual'), ('Google', 'Google'), ('Apple', 'Apple')], default='Manual', help_text='Type of Signup.', max_length=6)),
                ('social_login_token', models.CharField(blank=True, default=None, max_length=1000, null=True)),
                ('notification_token', models.CharField(blank=True, default=None, help_text='We will send the notification via this token.', max_length=300, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubPromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('max_uses', models.IntegerField(default=1)),
                ('uses', models.IntegerField(default=0)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('phase', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_receiver', to=settings.AUTH_USER_MODEL)),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_maker', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.projects')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('feedback', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customerprofile')),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('reward', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('is_redeemed', models.BooleanField(default=False)),
                ('referred_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referred_by', to=settings.AUTH_USER_MODEL)),
                ('referrer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrerals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('due_date', models.DateField()),
                ('completed', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='milestones', to='core.projects')),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.projects')),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FeaturedListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_featured', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EngagementLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employees', models.ManyToManyField(blank=True, related_name='company_employees', to=settings.AUTH_USER_MODEL)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
