from django.shortcuts import render, redirect
from .models import Buyer, Game
from .forms import  UserRegister

def platform(request):
    return render(request, 'fourth_task/platform.html')

def games(request):
    games = Game.objects.all()
    return render(request, 'fourth_task/games.html', {'games': games})

def cart(request):
    return render(request, 'fourth_task/cart.html')


def sign_up_by_html(request):
    info = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')

        if password != repeat_password:
            info['error'] = 'Пароли не совпадают'
        elif not age.isdigit() or int(age) < 18:
            info['error'] = 'Вы должны быть старше 18'
        elif Buyer.objects.filter(name=username).exists():
            info['error'] = 'Пользователь уже существует'
        else:
            Buyer.objects.create(name=username, balance=0, age=int(age))
            return redirect('succes', username=username)

    return render(request, 'fifth_task/registration_page.html', info)

def sign_up_by_django(request):
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']

            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif Buyer.objects.filter(name=username).exists():
                info['error'] = 'Пользователь уже существует'
            else:
                return redirect('succes', username=username)
        else:
            info['error'] = 'Проверьте введенные данные'

    info['form'] = UserRegister()
    return render(request, 'fifth_task/registration_page.html', info)

def succes(request, username):
    return render(request, 'fifth_task/succes.html', {'username': username})
