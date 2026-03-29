import json
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import School, Classroom, Assignment, DailyChallenge, ChallengeCompletion, PaymentOrder
from .decorators import teacher_required
from .exports import export_class_csv
from modules.models import Module

User = get_user_model()


@teacher_required
def school_dashboard(request):
    """Teacher's school overview — classrooms, quick stats, recent activity."""
    school = getattr(request, 'school', None)
    classrooms = Classroom.objects.filter(teacher=request.user).select_related('school')
    if school:
        all_classrooms = Classroom.objects.filter(school=school).select_related('teacher')
    else:
        all_classrooms = classrooms

    context = {
        'classrooms': classrooms,
        'all_classrooms': all_classrooms,
        'school': school,
        'total_students': sum(c.students.count() for c in classrooms),
    }
    return render(request, 'school/dashboard.html', context)


@teacher_required
def classroom_detail(request, classroom_id):
    """Classroom view: student table, assignments, class leaderboard."""
    classroom = get_object_or_404(Classroom, pk=classroom_id)

    # Only teacher of this classroom or school_admin may view
    if request.user.role not in ('admin', 'school_admin') and classroom.teacher != request.user:
        messages.error(request, 'You do not have access to this classroom.')
        return redirect('/school/')

    students = classroom.students.all().order_by('first_name', 'last_name')
    assignments = classroom.assignments.select_related('module').order_by('-created_at')

    # Build leaderboard from gamification (graceful fallback)
    leaderboard = []
    for s in students:
        try:
            from gamification.models import UserXP
            xp_obj = UserXP.objects.filter(user=s).first()
            xp = xp_obj.total_xp if xp_obj else 0
            level = xp_obj.level if xp_obj else 1
        except Exception:
            xp = level = 0
        leaderboard.append({'user': s, 'xp': xp, 'level': level})
    leaderboard.sort(key=lambda x: x['xp'], reverse=True)

    context = {
        'classroom': classroom,
        'students': students,
        'assignments': assignments,
        'leaderboard': leaderboard[:10],
    }
    return render(request, 'school/classroom_detail.html', context)


@teacher_required
def student_report(request, classroom_id, student_id):
    """Per-student drill-down for a teacher."""
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    student = get_object_or_404(User, pk=student_id)

    try:
        from gamification.models import UserXP
        from modules.models import UserProgress
        profile = UserXP.objects.filter(user=student).first()
        progress_qs = UserProgress.objects.filter(user=student).select_related('module').order_by('-last_accessed')
    except Exception:
        profile = None
        progress_qs = []

    context = {
        'classroom': classroom,
        'student': student,
        'profile': profile,
        'progress_list': progress_qs,
    }
    return render(request, 'school/student_report.html', context)


@teacher_required
def create_classroom(request):
    """Create a new classroom."""
    school = getattr(request, 'school', None)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        grade = request.POST.get('grade', '')
        if name and grade:
            classroom = Classroom.objects.create(
                school=school or _get_or_create_demo_school(request.user),
                teacher=request.user,
                name=name,
                grade=int(grade),
            )
            messages.success(request, f'Classroom "{name}" created! Join code: {classroom.join_code}')
            return redirect(f'/school/classroom/{classroom.pk}/')
        else:
            messages.error(request, 'Please provide a classroom name and grade.')
    return render(request, 'school/create_classroom.html', {'school': school})


def _get_or_create_demo_school(user):
    """Fallback: create a demo school for a teacher without a school FK."""
    school, _ = School.objects.get_or_create(
        name='Demo School',
        defaults={
            'city': 'India',
            'contact_email': user.email,
            'subscription_tier': 'free',
        }
    )
    return school


def _get_or_create_personal_school(user):
    """Get or create a personal school for an individual user (no school linked)."""
    name = f"{user.get_full_name() or user.email} (Personal)"
    school, _ = School.objects.get_or_create(
        contact_email=user.email,
        name=name,
        defaults={
            'city': 'India',
            'subscription_tier': 'free',
        }
    )
    return school


@teacher_required
def create_assignment(request, classroom_id):
    """Assign a module to a classroom."""
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    modules = Module.objects.filter(is_published=True).order_by('order')

    if request.method == 'POST':
        module_id = request.POST.get('module_id')
        title = request.POST.get('title', '').strip()
        instructions = request.POST.get('instructions', '').strip()
        due_date_str = request.POST.get('due_date', '')
        status = request.POST.get('status', 'active')

        if module_id and title:
            module = get_object_or_404(Module, pk=module_id)
            due_date = None
            if due_date_str:
                from datetime import date
                try:
                    due_date = date.fromisoformat(due_date_str)
                except ValueError:
                    pass

            Assignment.objects.create(
                classroom=classroom,
                module=module,
                title=title,
                instructions=instructions,
                due_date=due_date,
                status=status,
                created_by=request.user,
            )
            messages.success(request, f'Assignment "{title}" created.')
            return redirect(f'/school/classroom/{classroom_id}/')

    return render(request, 'school/create_assignment.html', {
        'classroom': classroom,
        'modules': modules,
    })


@login_required
def join_classroom(request, code):
    """Student self-enrollment via 8-char join code."""
    classroom = get_object_or_404(Classroom, join_code=code.upper())

    if request.user in classroom.students.all():
        messages.info(request, f'You are already in {classroom.name}!')
        return redirect('/')

    classroom.students.add(request.user)

    # Set school FK on user if not set
    if hasattr(request.user, 'school_id') and not request.user.school_id:
        request.user.school = classroom.school
        request.user.save(update_fields=['school'])

    messages.success(request, f'Welcome to {classroom.school.name} — {classroom.name}! 🎉')
    return redirect('/')


@teacher_required
def export_class_report(request, classroom_id, fmt='csv'):
    """Download class report as CSV."""
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    return export_class_csv(classroom)


# ─── Razorpay Payment Views ───────────────────────────────────────────────────

@login_required
def payment_page(request):
    """Subscription upgrade page with Razorpay checkout — open to all users."""
    school = getattr(request, 'school', None)
    if not school:
        school = _get_or_create_personal_school(request.user)

    recent_orders = PaymentOrder.objects.filter(school=school).order_by('-created_at')[:5]
    try:
        initial_students = max(1, int(request.GET.get('students', 1)))
    except (ValueError, TypeError):
        initial_students = 1
    autostart = request.GET.get('autostart') == '1' and bool(settings.RAZORPAY_KEY_ID)
    initial_price = (
        settings.RAZORPAY_PRICE_PER_STUDENT_BULK
        if initial_students >= settings.RAZORPAY_BULK_THRESHOLD
        else settings.RAZORPAY_PRICE_PER_STUDENT
    )
    context = {
        'school': school,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'price_per_student': settings.RAZORPAY_PRICE_PER_STUDENT,
        'price_per_student_bulk': settings.RAZORPAY_PRICE_PER_STUDENT_BULK,
        'bulk_threshold': settings.RAZORPAY_BULK_THRESHOLD,
        'recent_orders': recent_orders,
        'initial_students': initial_students,
        'initial_total': initial_students * initial_price,
        'autostart': autostart,
        'features': [
            'Live Claude AI Tutor',
            '15+ Interactive Labs',
            '7 AI/ML Modules',
            'Gamification & Leaderboards',
            'Teacher Dashboard & Reports',
            'Class Join Code',
            'Priority Support',
            'GST Invoice Included',
        ],
    }
    return render(request, 'school/payment.html', context)


@login_required
@require_POST
def create_razorpay_order(request):
    """Create a Razorpay order and return its details as JSON."""
    try:
        import razorpay
    except ImportError:
        return JsonResponse({'error': 'Razorpay package not installed. Run: pip install razorpay'}, status=500)

    school = getattr(request, 'school', None)
    if not school:
        school = _get_or_create_personal_school(request.user)

    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return JsonResponse({'error': 'Razorpay credentials not configured. Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET.'}, status=500)

    try:
        student_count = max(1, int(request.POST.get('student_count', 1)))
        plan = request.POST.get('plan', 'annual')
        if plan not in dict(School.TIER_CHOICES):
            plan = 'annual'
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid student count.'}, status=400)

    if student_count >= settings.RAZORPAY_BULK_THRESHOLD:
        price = settings.RAZORPAY_PRICE_PER_STUDENT_BULK
    else:
        price = settings.RAZORPAY_PRICE_PER_STUDENT
    amount_paise = student_count * price * 100  # INR → paise

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    try:
        razorpay_order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': f'school_{school.pk}_{plan}',
            'notes': {
                'school_id': str(school.pk),
                'school_name': school.name,
                'plan': plan,
                'student_count': str(student_count),
            },
        })
    except Exception as e:
        return JsonResponse({'error': f'Razorpay order creation failed: {str(e)}'}, status=500)

    PaymentOrder.objects.create(
        school=school,
        created_by=request.user,
        razorpay_order_id=razorpay_order['id'],
        amount=amount_paise,
        currency='INR',
        plan=plan,
        student_count=student_count,
    )

    return JsonResponse({
        'order_id': razorpay_order['id'],
        'amount': amount_paise,
        'currency': 'INR',
        'key_id': settings.RAZORPAY_KEY_ID,
        'school_name': school.name,
        'contact_email': school.contact_email,
        'contact_phone': school.contact_phone or '',
    })


@login_required
@require_POST
def verify_payment(request):
    """Verify Razorpay payment signature and activate the subscription."""
    try:
        import razorpay
    except ImportError:
        return JsonResponse({'error': 'Razorpay package not installed.'}, status=500)

    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    razorpay_signature = request.POST.get('razorpay_signature', '')

    if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
        return JsonResponse({'success': False, 'error': 'Missing payment fields.'}, status=400)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        })
    except Exception:
        return JsonResponse({'success': False, 'error': 'Payment signature verification failed.'}, status=400)

    try:
        order = PaymentOrder.objects.get(razorpay_order_id=razorpay_order_id)
    except PaymentOrder.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found.'}, status=404)

    if order.status == 'paid':
        return JsonResponse({'success': True, 'message': 'Already activated.'})

    order.razorpay_payment_id = razorpay_payment_id
    order.razorpay_signature = razorpay_signature
    order.status = 'paid'
    order.paid_at = timezone.now()
    order.save()

    today = timezone.now().date()
    school = order.school
    school.subscription_tier = order.plan
    school.subscription_start = today
    school.subscription_end = today + timedelta(days=365)
    school.max_students = order.student_count
    school.save()

    return JsonResponse({
        'success': True,
        'message': f'Payment successful! {school.name} subscription activated until {school.subscription_end}.',
    })
