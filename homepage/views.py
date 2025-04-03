from django.shortcuts import render
from .models import FAQ


def homepage(request):
    """ View to return Homepage """
    return render(request, 'homepage/homepage.html')


def faq_view(request):
    """ View to return FAQ and Answers """
    faqs = FAQ.objects.all()
    return render(request, 'homepage.html', {"faq": faqs})