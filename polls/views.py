from django.shortcuts import render

def cheese(request):
    return render(request, 'polls/cheese.html')

def wine(request):
    return render(request, 'polls/wine.html')

def home(request):
    return render(request, 'polls/home.html')

def glossary(request):
    return render(request, 'polls/glossary.html')