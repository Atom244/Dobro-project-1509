from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from .forms import AppealForm
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
