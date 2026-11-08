from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


def contacts(request):
    from content.models import Contact
    return render(request, 'core/contacts.html', {'contacts': Contact.objects.all()})
