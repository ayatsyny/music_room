from django.shortcuts import render


def home(request):
    account_deezer = None
    # if request.user.is_authenticated:
        # account_deezer = AtachService.objects.filter(user=request.user, name='deezer').first()
    return render(request, 'home.html', {'account_deezer': account_deezer})

