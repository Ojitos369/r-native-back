from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'data': {
            'saludo': 'text from context from django'
        }
    }
    return render(request, 'main/index.html', context)