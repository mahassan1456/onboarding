from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


def home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('dashboard:master_dashboard'))
    return HttpResponseRedirect(reverse('dashboard:dashboard'))
    