from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AppealForm, StaffAppealUpdateForm
from .models import Appeal, AppealStatusHistory


@login_required
def create(request):
    form = AppealForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        appeal = form.save(commit=False)
        appeal.user = request.user
        appeal.save()
        AppealStatusHistory.objects.create(appeal=appeal, new_status=appeal.status, comment='Обращение зарегистрировано')
        return render(request, 'appeals/success.html', {'appeal': appeal})
    return render(request, 'appeals/create.html', {'form': form})


@login_required
def my_appeals(request):
    return render(request, 'appeals/list.html', {'appeals': Appeal.objects.filter(user=request.user)})


@login_required
def detail(request, public_id):
    appeal = get_object_or_404(Appeal, public_id=public_id)
    if appeal.user != request.user and not request.user.is_staff:
        raise PermissionDenied
    return render(request, 'appeals/detail.html', {'appeal': appeal})


def index(request):
    return render(request, 'appeals/index.html')


def staff_required(view):
    return user_passes_test(lambda user: user.is_active and user.is_staff, login_url='login')(view)


@staff_required
def staff_dashboard(request):
    appeals = Appeal.objects.select_related('user', 'category')
    status = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()
    if status:
        appeals = appeals.filter(status=status)
    if query:
        appeals = appeals.filter(
            Q(public_id__icontains=query) |
            Q(subject__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__username__icontains=query)
        )
    counts = Appeal.objects.values('status').annotate(total=Count('id'))
    status_counts = {item['status']: item['total'] for item in counts}
    context = {
        'appeals': appeals[:100],
        'status_counts': status_counts,
        'total_count': Appeal.objects.count(),
        'new_count': status_counts.get(Appeal.Status.NEW, 0),
        'in_progress_count': status_counts.get(Appeal.Status.IN_PROGRESS, 0),
        'resolved_count': status_counts.get(Appeal.Status.RESOLVED, 0),
        'status_choices': Appeal.Status.choices,
        'selected_status': status,
        'query': query,
    }
    return render(request, 'appeals/staff_dashboard.html', context)


@staff_required
@transaction.atomic
def staff_update(request, public_id):
    if request.method != 'POST':
        return redirect('staff-dashboard')
    appeal = get_object_or_404(Appeal, public_id=public_id)
    form = StaffAppealUpdateForm(request.POST, instance=appeal)
    if form.is_valid():
        old_status = appeal.status
        updated = form.save()
        if old_status != updated.status or form.cleaned_data['comment']:
            AppealStatusHistory.objects.create(
                appeal=updated,
                old_status=old_status,
                new_status=updated.status,
                comment=form.cleaned_data['comment'],
            )
    return redirect('staff-dashboard')
