# Generated by Django 3.2.25 on 2025-05-17 08:23

import Website.models
import ckeditor.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BecomeaPartnerDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BecomeaPartnerRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(default=None, max_length=255, verbose_name='Restaurant Name')),
                ('your_name', models.CharField(max_length=100, verbose_name='Your Name')),
                ('phone', models.CharField(blank=True, default=None, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed.", regex='^\\+?1?\\d{9,14}$')], verbose_name='Phone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('requested_at', models.DateTimeField(auto_now_add=True, verbose_name='Requested At')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessMainSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('logo', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_BusinessMainSection_image_path, verbose_name='Logo')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('link', models.URLField(verbose_name='Link')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default=None, max_length=255, verbose_name='Company Name')),
                ('your_name', models.CharField(max_length=100, verbose_name='Your Name')),
                ('phone', models.CharField(blank=True, default=None, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed.", regex='^\\+?1?\\d{9,14}$')], verbose_name='Phone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('requested_at', models.DateTimeField(auto_now_add=True, verbose_name='Requested At')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessSolutions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('image', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_BusinessSolutions_image_path, verbose_name='Image')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarearesDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarearesRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('your_name', models.CharField(max_length=100, verbose_name='Your Name')),
                ('phone', models.CharField(blank=True, default=None, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed.", regex='^\\+?1?\\d{9,14}$')], verbose_name='Phone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('your_role', models.CharField(blank=True, max_length=100, null=True, verbose_name='Your Role')),
                ('resume', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_Careares_Requests_Resumes_path, verbose_name='Resume')),
                ('requested_at', models.DateTimeField(auto_now_add=True, verbose_name='Requested At')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255, verbose_name='Location')),
                ('phone', models.CharField(blank=True, default=None, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed.", regex='^\\+?1?\\d{9,14}$')], verbose_name='Phone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('image', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_Contact_images_path, verbose_name='Image')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiscoverUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('sub_title', models.CharField(default=None, max_length=100, verbose_name='Sub Title')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('image', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_DiscoverUs_image_path, verbose_name='Image')),
                ('last_update', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DownloadApps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('image', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_DownloadApps_image_path, verbose_name='Image')),
                ('link', models.URLField(verbose_name='Link')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('type', models.CharField(choices=[('General', 'General'), ('Process', 'Process'), ('Payments', 'Payments'), ('Security', 'Security')], default='General', max_length=8)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HowItWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default=None, max_length=100, verbose_name='Number')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MainAnimation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('small_image', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_MainAnimation_image_path, verbose_name='Small Image')),
                ('animate_image', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_MainAnimation_image_path, verbose_name='Animate Image')),
                ('image', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_MainAnimation_image_path, verbose_name='Image')),
                ('last_update', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MetaTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(choices=[('Home', 'Home'), ('Business', 'Business'), ('Become', 'Become a partner'), ('Careers', 'Careers'), ('Contact', 'Contact us'), ('Privacy', 'Privacy'), ('Error', 'Error')], default='Home', help_text='Page name', max_length=20)),
                ('title', models.CharField(help_text='Page title', max_length=255)),
                ('description', models.TextField(help_text='Page description')),
                ('keywords', models.CharField(help_text='Comma-separated keywords', max_length=255)),
                ('author', models.CharField(blank=True, help_text='Author name', max_length=255)),
                ('robots', models.CharField(default='index,follow', help_text='Robots instructions', max_length=255)),
                ('language', models.CharField(default='en-US', help_text='Content language', max_length=7)),
                ('viewport', models.CharField(default='width=device-width,initial-scale=1', help_text='Viewport settings', max_length=255)),
                ('og_title', models.CharField(blank=True, help_text='Open Graph title', max_length=255)),
                ('og_description', models.TextField(blank=True, help_text='Open Graph description')),
                ('og_type', models.CharField(blank=True, help_text='Open Graph content type', max_length=255)),
                ('og_url', models.URLField(blank=True, help_text='Open Graph URL')),
                ('og_image', models.ImageField(blank=True, help_text='Open Graph image', upload_to=Website.models.upload_MetaTags_Images_path)),
                ('twitter_card', models.CharField(blank=True, help_text='Twitter Card type', max_length=255)),
                ('twitter_title', models.CharField(blank=True, help_text='Twitter Card title', max_length=255)),
                ('twitter_description', models.TextField(blank=True, help_text='Twitter Card description')),
                ('twitter_image', models.ImageField(blank=True, help_text='Twitter Card image', upload_to=Website.models.upload_MetaTags_Images_path)),
                ('apple_mobile_web_app_capable', models.CharField(blank=True, help_text='Apple mobile web app settings', max_length=255)),
                ('theme_color', models.CharField(blank=True, help_text='Browser tab/toolbar color', max_length=7)),
                ('msapplication_tap_highlight', models.CharField(default='#cccccc', max_length=255)),
                ('use_facebook', models.BooleanField(default=False)),
                ('facebook_app_id', models.CharField(blank=True, help_text='Facebook App ID', max_length=255)),
                ('custom_namespace', models.CharField(blank=True, max_length=255)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Meta Tag',
                'verbose_name_plural': 'Meta Tags',
            },
        ),
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('description', ckeditor.fields.RichTextField(default=None, verbose_name='Description')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Slogan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slogan', models.CharField(default=None, max_length=100, verbose_name='Slogan')),
                ('short_slogan', models.CharField(default=None, max_length=100, verbose_name='Short Slogan')),
                ('last_update', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Social_Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('image', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_Social_Media_image_path, verbose_name='Image')),
                ('link', models.URLField(verbose_name='Link')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WhyUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, default=None, null=True, upload_to=Website.models.upload_WhyUs_image_path, verbose_name='Image')),
                ('title', models.CharField(default=None, max_length=100, verbose_name='Title')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('last_update', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
