from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import SchoolInquiryForm
from .models import SchoolInquiry
from modules.models import Module

FAQ_ITEMS = [
    (
        "Does my child need prior coding knowledge?",
        "Not at all. Class 7 starts with Python basics from scratch. Class 8–10 begins with logic and patterns. Every track is designed for complete beginners."
    ),
    (
        "How do students join?",
        "The teacher shares a simple join code on WhatsApp or the classroom board. Students open it in any browser — no app download, no setup."
    ),
    (
        "Is it aligned with CBSE / ICSE?",
        "Yes. Content maps to CBSE, ICSE, and NEP 2020 AI curriculum guidelines. State board schools also find it directly applicable."
    ),
    (
        "How do we pay?",
        "UPI, NEFT/RTGS, or Razorpay link. GST invoice provided. No international card needed."
    ),
]


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        form = SchoolInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            # Notify Quantinodes team about new school inquiry
            try:
                send_mail(
                    subject=f'New School Inquiry — {inquiry.school_name} ({inquiry.city})',
                    message=(
                        f'New school inquiry received on Quantinodes.\n\n'
                        f'School: {inquiry.school_name}\n'
                        f'City: {inquiry.city}\n'
                        f'Contact: {inquiry.contact_name}\n'
                        f'Phone: {inquiry.contact_phone}\n'
                        f'Email: {inquiry.contact_email}\n'
                        f'Students: {inquiry.student_count}\n'
                        f'Plan Interest: {inquiry.interested_plan}\n'
                        f'Message: {inquiry.message or "—"}\n'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['quantinodes@gmail.com', 'info@quantinodes.com'],
                    fail_silently=True,
                )
            except Exception:
                pass
            return redirect('/thank-you/')
    else:
        form = SchoolInquiryForm()

    python_modules = Module.objects.filter(is_published=True, grade_level='7').order_by('order')
    ai_modules = Module.objects.filter(is_published=True, grade_level='all').order_by('order')
    modules = list(python_modules) + list(ai_modules)
    inquiry_count = SchoolInquiry.objects.count()

    return render(request, 'landing/index.html', {
        'form': form,
        'modules': modules,
        'inquiry_count': inquiry_count,
        'faq_items': FAQ_ITEMS,
    })


def thank_you(request):
    return render(request, 'landing/thank_you.html')
