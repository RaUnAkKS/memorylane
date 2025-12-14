from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm,CapsuleForm,CapsuleCommentForm,CollaboratorForm,CapsuleEntryForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Capsule,Notification
from django.db.models import Q
from django.utils import timezone
from .utils import create_unlock_notifications
from django.http import JsonResponse


# Create your views here.
def home_view(request):
    return render(request,'app/home.html')

@login_required
def dashboard_view(request):
    return render(request,'app/dashboard.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid:
            user = form.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Input')
    else:
        form = SignupForm()
        context = {'form':form}
        return render(request,'app/signup.html',context)
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_capsule(request):
    if request.method == 'POST':
        form = CapsuleForm(request.POST, request.FILES)
        if form.is_valid():
            capsule = form.save(commit=False)
            capsule.created_by = request.user
            capsule.save()
            form.save_m2m() 
            return redirect('dashboard')
    else:
        form = CapsuleForm()
        context = {'form' : form}

    return render(request, 'app/create_capsule.html',context)

@login_required
def capsule_list(request):
    user = request.user

    capsules = Capsule.objects.filter(
        Q(created_by=user) |
        Q(recipients=user) |
        Q(collaborators=user)
    ).distinct()

    # FILTER LOGIC
    privacy = request.GET.get('privacy')
    status = request.GET.get('status')

    if privacy:
        capsules = capsules.filter(privacy=privacy)

    if status == 'locked':
        capsules = capsules.filter(unlock_date__gt=timezone.now())
    elif status == 'unlocked':
        capsules = capsules.filter(unlock_date__lte=timezone.now())

    context = {
        'capsules': capsules,
        'selected_privacy': privacy,
        'selected_status': status,
    }

    return render(request, 'app/capsule_list.html', context)


def capsule_detail(request,capsule_id):
    capsule = get_object_or_404(Capsule,id=capsule_id)
    user = request.user
    context = {'capsule' : capsule}
    if capsule.privacy == 'public':
        return render(request,'app/capsule_detail.html',context)
    if not request.user.is_authenticated:
        return redirect('login')
    if capsule.privacy == 'private' and request.user!=capsule.created_by:
        messages.error(request,'You are not allowed to view this capsule')
        return redirect('capsule_list')
    if capsule.privacy == 'family':
        allowed_users = (
            list(capsule.recipients.all())+list(capsule.collaborators.all())+[capsule.created_by]
        )
        if request.user not in allowed_users:
            messages.error(request,'You are not allowed to view this capsule')
            return redirect('capsule_list')

    comment_form = None

    if capsule.is_unlocked():
        if request.method == 'POST':
            comment_form = CapsuleCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.capsule = capsule
                comment.user = user
                comment.save()
                return redirect('capsule_detail', capsule_id=capsule.id)
        else:
            comment_form = CapsuleCommentForm()

    comments = capsule.comments.all().order_by('-created_at')

    context = {
        'capsule': capsule,
        'comments': comments,
        'comment_form': comment_form,
    }

    if capsule.is_unlocked() and not capsule.notification_sent:
        create_unlock_notifications(capsule)
        capsule.notification_sent = True
        capsule.save()

    Notification.objects.filter(
        user=request.user,
        capsule=capsule,
        is_read=False
    ).update(is_read=True)

    return render(request, 'app/capsule_detail.html', context)


@login_required
def manage_collaborators(request, capsule_id):
    capsule = get_object_or_404(Capsule, id=capsule_id)

    if request.user != capsule.created_by:
        messages.error(request, "Only the creator can manage collaborators.")
        return redirect('capsule_detail', capsule_id=capsule.id)

    if request.method == 'POST':
        form = CollaboratorForm(request.POST,instance=capsule,user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Collaborators updated successfully.")
            return redirect('capsule_detail', capsule_id=capsule.id)
    else:
        form = CollaboratorForm(instance=capsule,user=request.user)

    context = {'capsule':capsule,'form':form}
    return render(request,'app/manage_collaborators.html',context)

@login_required
def add_entry(request, capsule_id):
    capsule = get_object_or_404(Capsule, id=capsule_id)
    user = request.user
    allowed_users = (
        list(capsule.collaborators.all()) +
        list(capsule.recipients.all()) +
        [capsule.created_by]
    )

    if user not in allowed_users:
        messages.error(request, "You cannot contribute to this capsule.")
        return redirect('capsule_detail', capsule_id=capsule.id)

    if not capsule.is_unlocked():
        messages.error(request, "Capsule is still locked.")
        return redirect('capsule_detail', capsule_id=capsule.id)

    if request.method == 'POST':
        form = CapsuleEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.capsule = capsule
            entry.created_by = user
            entry.save()
            return redirect('capsule_detail', capsule_id=capsule.id)
        else:
            messages.error(request,'Invalid Inputs')
            return redirect('capsule_detail', capsule_id=capsule.id)
    else:
        form = CapsuleEntryForm()

    return render(
        request,'app/add_entry.html',{'form': form, 'capsule': capsule})

@login_required
def trigger_event(request, capsule_id):
    capsule = get_object_or_404(Capsule, id=capsule_id)

    if request.user != capsule.created_by:
        messages.error(request, "Only the creator can trigger this event.")
        return redirect('capsule_detail', capsule_id=capsule.id)

    if capsule.unlock_type != 'event':
        messages.error(request, "This capsule is not event-based.")
        return redirect('capsule_detail', capsule_id=capsule.id)

    capsule.event_triggered = True
    capsule.save()

    messages.success(request, "🎉 Event triggered! Capsule unlocked.")
    return redirect('capsule_detail', capsule_id=capsule.id)

@login_required
def notifications(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(
        request,
        'app/notifications.html',
        {'notifications': notifications}
    )

@login_required
def notification_count_api(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})

