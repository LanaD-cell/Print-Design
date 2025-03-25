from django.shortcuts import render

# Create your views here.
def homepage(request):
    """ View to return Homepage """
    return render(request, 'homepage/homepage.html')