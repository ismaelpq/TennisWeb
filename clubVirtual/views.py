from django.shortcuts import render

# Create your views here.
def clubVirtual(request):
    return render(request, 'clubVirtual/homeClubVirtual.html')
