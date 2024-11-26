from django.shortcuts import render
from django.http import JsonResponse
from .models import *

# Create your views here.

def Home(request):
    mainAnimation = MainAnimation.objects.all()
    slogan = Slogan.objects.all().first()
    whyUs = WhyUs.objects.all()
    discoverUs = DiscoverUs.objects.all()
    howItWork = HowItWork.objects.all()
    socialMedia = Social_Media.objects.all()
    downloadApps = DownloadApps.objects.all()
    AppleStore = DownloadApps.objects.filter(title="Apple Store").first()
    GooglePlay = DownloadApps.objects.filter(title="Google Play").first()
    meta = MetaTags.objects.filter(page="Home").first()

    general_faq = FAQ.objects.filter(type="General")
    process_faq = FAQ.objects.filter(type="Process")
    payments_faq = FAQ.objects.filter(type="Payments")
    security_faq = FAQ.objects.filter(type="Security")

    context = {
        'MainAnimation': mainAnimation,
        'slogan': slogan,
        'whyUs': whyUs,
        'discoverUs': discoverUs,
        'HowItWork': howItWork,
        'SocialMedia': socialMedia,
        'DownloadApps': downloadApps,
        'general_faq': general_faq,
        'process_faq': process_faq,
        'payments_faq': payments_faq,
        'security_faq': security_faq,
        'AppleStore': AppleStore,
        'GooglePlay': GooglePlay,
        'meta_tags': meta,
    }
    return render(request, 'index.html', context)

def Business(request):
    businessMainSection = BusinessMainSection.objects.all().first()
    businessSolutions = BusinessSolutions.objects.all()
    businessStatistics = BusinessStatistics.objects.all()
    social_Media = Social_Media.objects.all()
    downloadApps = DownloadApps.objects.all()
    AppleStore = DownloadApps.objects.filter(title="Apple Store").first()
    meta = MetaTags.objects.filter(page_name="Business").first()
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        your_name = request.POST.get('your_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        description = request.POST.get('Description')  # Note the difference in the field name
        try:
            BusinessRequests.objects.create(
                company_name=company_name,
                your_name=your_name,
                phone=phone_number,
                email=email,
                description=description,

            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    context = {
        'businessMainSection': businessMainSection,
        'businessSolutions': businessSolutions,
        'businessStatistics': businessStatistics,
        'downloadApps': downloadApps,
        'Social_Media': social_Media,
        'AppleStore': AppleStore,
        'meta_tags': meta,
    }
    return render(request, 'business.html', context)
#---------------------------------------------------End Business--------------------------------------------------------



#-------------------------------------------------Start Become_partner--------------------------------------------------
def Become_partner(request):
    becomeaPartnerDescription= BecomeaPartnerDescription.objects.all().first()
    social_Media = Social_Media.objects.all()
    downloadApps = DownloadApps.objects.all()
    AppleStore = DownloadApps.objects.filter(title="Apple Store").first()
    meta = MetaTags.objects.filter(page_name="Become").first()

    if request.method == 'POST':
        restaurant_name = request.POST.get('restaurant_name')
        your_name = request.POST.get('your_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        try:
            BecomeaPartnerRequests.objects.create(
                restaurant_name=restaurant_name,
                your_name=your_name,
                phone=phone_number,
                email=email,
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    context = {
        'becomeaPartnerDescription': becomeaPartnerDescription,
        'downloadApps': downloadApps,
        'Social_Media': social_Media,
        'AppleStore': AppleStore,
        'meta_tags': meta,
    }
    return render(request, 'become-partner.html', context)
#---------------------------------------------------End Become_partner--------------------------------------------------



#-------------------------------------------------Start Careers---------------------------------------------------------
def Careers(request):
    carearesDescription = CarearesDescription.objects.all().first()
    social_Media = Social_Media.objects.all()
    downloadApps = DownloadApps.objects.all()
    AppleStore = DownloadApps.objects.filter(title="Apple Store").first()
    meta = MetaTags.objects.filter(page_name="Careers").first()

    if request.method == 'POST':
        your_name = request.POST.get('your_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        your_role = request.POST.get('your_role')
        worker_resume = request.FILES.get('worker_resume')
        try:
            CarearesRequests.objects.create(
                your_name=your_name,
                phone=phone_number,
                email=email,
                your_role=your_role,
                resume=worker_resume,
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    context = {
        'downloadApps': downloadApps,
        'Social_Media': social_Media,
        'AppleStore': AppleStore,
        'carearesDescription': carearesDescription,
        'meta_tags': meta,
    }
    return render(request, 'careers.html', context)
#---------------------------------------------------End Careers---------------------------------------------------------



#-------------------------------------------------Start Contact---------------------------------------------------------
def Contact(request):
    contact = ContactUs.objects.all().first()
    social_Media = Social_Media.objects.all()
    downloadApps = DownloadApps.objects.all()
    AppleStore = DownloadApps.objects.filter(title="Apple Store").first()
    meta = MetaTags.objects.filter(page_name="Contact").first()

    context = {
        'contact': contact,
        'downloadApps': downloadApps,
        'Social_Media': social_Media,
        'AppleStore': AppleStore,
        'meta_tags': meta,
    }
    return render(request, 'contact.html', context)
#---------------------------------------------------End Contact---------------------------------------------------------



#-------------------------------------------------Start Privacy---------------------------------------------------------
def Privacy_view(request):
    privacy_obj = Privacy.objects.all().first()
    social_Media = Social_Media.objects.all()
    downloadApps = DownloadApps.objects.all()
    AppleStore = DownloadApps.objects.filter(title="Apple Store").first()
    meta = MetaTags.objects.filter(page_name="Privacy").first()

    context = {
        'privacy': privacy_obj,
        'downloadApps': downloadApps,
        'Social_Media': social_Media,
        'AppleStore': AppleStore,
        'meta_tags': meta,
    }
    return render(request, 'privacy.html', context)
#---------------------------------------------------End Privacy---------------------------------------------------------



#-------------------------------------------------Start error_404-------------------------------------------------------
def error_404(request):
    social_Media = Social_Media.objects.all()
    downloadApps = DownloadApps.objects.all()
    AppleStore = DownloadApps.objects.filter(title="Apple Store").first()
    meta = MetaTags.objects.filter(page_name="Error").first()

    context = {
        'downloadApps': downloadApps,
        'Social_Media': social_Media,
        'AppleStore': AppleStore,
        'meta_tags': meta,
    }
    return render(request, '404.html', context)
#---------------------------------------------------End error_404-------------------------------------------------------
