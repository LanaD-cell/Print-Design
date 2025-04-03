from django.shortcuts import render
from .models import FAQ


def homepage(request):
    """ View to return Homepage and FAQ """
    faqs = FAQ.objects.all()
    return render(request, 'homepage/homepage.html', {'faqs': faqs})
