from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from .models import Task
import json


# ========================
# 🔐 AUTH VIEWS
# ========================

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        email = request.POST.get('email').strip()

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists!'})

        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect(reverse('App_Todo:task_list'))

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse('App_Todo:task_list'))
        return render(request, 'login.html', {'error': 'Wrong username or password!'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('App_Todo:login'))


# ========================
# 🔥 STREAK LOGIC
# ========================

def get_streak(user):
    today = timezone.now().date()
    streak = 0
    current_date = today

    while True:
        task_done = Task.objects.filter(
            user=user,
            date=current_date,
            completed=True
        ).exists()

        if task_done:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break

    return streak


# ========================
# ✅ TASK VIEWS
# ========================

@login_required(login_url='/login/')
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-id')
    return render(request, 'task_list.html', {'tasks': tasks})


@csrf_exempt
@login_required(login_url='/login/')
def task_create(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            description = data.get('description', '').strip()
            date = data.get('date')
            hours = data.get('hours') or 0

            if title:
                Task.objects.create(
                    user=request.user,
                    title=title,
                    description=description,
                    date=date,
                    hours=hours
                )
                return JsonResponse({"message": "Task created!"}, status=201)
            return JsonResponse({"error": "Title cannot be empty."}, status=400)

        else:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            date = request.POST.get('date')
            hours = request.POST.get('hours') or 0

            if title:
                Task.objects.create(
                    user=request.user,
                    title=title,
                    description=description,
                    date=date,
                    hours=hours
                )
                return redirect(reverse('App_Todo:task_list'))

            return render(request, 'task_form.html', {'error': "Title cannot be empty."})

    return render(request, 'task_form.html')


@login_required(login_url='/login/')
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title').strip()
        description = request.POST.get('description').strip()
        completed = request.POST.get('completed') == 'on'
        date = request.POST.get('date')
        hours = request.POST.get('hours') or 0

        task.completed = completed
        if title:
            task.title = title
            task.description = description
            task.date = date
            task.hours = hours
            task.save()
            return redirect(reverse('App_Todo:task_list'))

        return render(request, 'task_form.html', {
            'task': task,
            'error': "Title cannot be empty."
        })

    return render(request, 'task_form.html', {'task': task})


@login_required(login_url='/login/')
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect(reverse('App_Todo:task_list'))


@login_required(login_url='/login/')
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect(reverse('App_Todo:task_list'))


# ========================
# 📊 DASHBOARD
# ========================

@login_required(login_url='/login/')
def dashboard(request):
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)

    tasks = Task.objects.filter(user=request.user, date__gte=last_30_days)
    daily_data = tasks.filter(completed=True).values('date').annotate(count=Count('id')).order_by('date')

    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, completed=True).count()
    pending_tasks = Task.objects.filter(user=request.user, completed=False).count()
    total_hours = sum(t.hours for t in Task.objects.filter(user=request.user) if t.hours)

    days_studied = tasks.filter(completed=True).values('date').distinct().count()
    consistency = "On Track ✅" if days_studied >= 10 else "Off Track ❌"

    streak = get_streak(request.user)

    labels = [str(d['date']) for d in daily_data]
    data = [d['count'] for d in daily_data]

    return render(request, 'dashboard.html', {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'total_hours': total_hours,
        'consistency': consistency,
        'days_studied': days_studied,
        'labels': labels,
        'data': data,
        'streak': streak,
    })


# ========================
# 📧 WEEKLY REPORT
# ========================

@login_required(login_url='/login/')
def weekly_report(request):
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)

    tasks = Task.objects.filter(
        user=request.user,
        date__gte=last_7_days
    )

    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()
    total_hours = sum(t.hours for t in tasks if t.hours)
    streak = get_streak(request.user)

    # Email bhejo
    if request.user.email:
        message = f"""
Helo {request.user.username}! 👋

Tumhari is hafte ki report:

📌 Total Tasks: {total}
✅ Completed: {completed}
⏳ Pending: {pending}
⏱️ Total Hours Studied: {total_hours} hrs
🔥 Current Streak: {streak} days

{"On Track ✅ - Zabardast!" if completed >= 5 else "Off Track ❌ - Aur mehnat karo!"}

Keep going! 💪
        """

        send_mail(
            subject='📊 Tumhari Weekly Study Report',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
        )
        return JsonResponse({"message": f"Weekly report {request.user.email} pe bhej di!"})

    return JsonResponse({"error": "Email set nahi hai tumhare account mein!"})


# ========================
# 🔔 OTHER APIs
# ========================

@login_required(login_url='/login/')
def check_consistency(request):
    today = timezone.now().date()
    last_15_days = today - timedelta(days=15)

    tasks = Task.objects.filter(
        user=request.user,
        date__gte=last_15_days,
        completed=True
    )

    days = tasks.values('date').distinct().count()
    status = "On Track" if days >= 10 else "Off Track"

    return JsonResponse({"status": status, "days_completed": days})


@login_required(login_url='/login/')
def daily_reminder(request):
    today = timezone.now().date()

    task_done = Task.objects.filter(
        user=request.user,
        date=today,
        completed=True
    ).exists()

    if not task_done:
        return JsonResponse({"message": "⚠️ You have not studied today"})
    return JsonResponse({"message": "✅ Good job, keep going!"})


def streak_api(request):
    if request.user.is_authenticated:
        streak = get_streak(request.user)
        return JsonResponse({"streak": streak, "message": f"🔥 {streak} day streak!"})
    return JsonResponse({"error": "Login karo pehle!"}, status=401)