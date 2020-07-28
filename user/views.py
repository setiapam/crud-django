import math
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from .forms import *


# Create your views here.
def home(request):
    if not request.session.exists(request.session.session_key):
        return redirect('login')
    else:
        form = UserForm()
        ctx = {'form': form}
        return render(request, 'table.html', ctx)


def register(request):
    form = UserForm()
    ctx = {'form': form}
    return render(request, 'register.html', ctx)


def logout(request):
    request.session.delete()
    return redirect('login')


def login(request):
    if request.is_ajax() and request.method == 'POST':
        login_form = LoginForm(request.POST)
        try:
            user = User.objects.get(email=request.POST['email'])
        except User.DoesNotExist:
            user = None
        if not user:
            return JsonResponse({'error': True, 'msg': 'user does not exist'})
        else:
            if login_form.is_valid():
                if check_password(login_form.cleaned_data['password'], user.password):
                    request.session['logged_in'] = True
                    request.session['email'] = login_form.cleaned_data['email']
                    return JsonResponse({'error': False, 'msg': 'success', 'url': reverse('home')})
                else:
                    return JsonResponse({'error': True, 'msg': 'wrong password'})
            else:
                return JsonResponse({'error': True, 'msg': login_form.errors})
    else:
        form = LoginForm()
        ctx = {'form': form}
        return render(request, 'login.html', ctx)


def add_user(request):
    if request.is_ajax() and request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            clearPassNoHash = form.cleaned_data['password']
            hashed = make_password(clearPassNoHash, None, 'default')
            user = form.save()
            user.password = hashed
            user.save()
            return JsonResponse({'error': False, 'msg': 'yeee'})
        else:
            return JsonResponse({'error': True, 'msg': form.errors})
    else:
        form = UserForm()
        ctx = {'form': form}
        return render(request, 'main.html', ctx)


def mainTableData(request):
    if not request.session.exists(request.session.session_key):
        return redirect('login')
    else:
        persons = User.objects.all()
        total = persons.count()

        _start = request.GET.get('start')
        _length = request.GET.get('length')
        if _start and _length:
            start = int(_start)
            length = int(_length)
            page = math.ceil(start / length) + 1
            per_page = length

            persons = persons[start:start + length]

        data = [person.to_dict_json() for person in persons]
        response = {
            'data': data,
            'page': page,
            'per_page': per_page,
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)


def update_user(request, pk):
    if not request.session.exists(request.session.session_key):
        return redirect('login')
    else:
        user = User.objects.get(id=pk)
        update_form = UserForm(instance=user)
        if request.is_ajax() and request.method == 'POST':
            update_form = UserForm(request.POST, request.FILES, instance=user)
            if update_form.is_valid():
                clearPassNoHash = update_form.cleaned_data['password']
                hashed = make_password(clearPassNoHash, None, 'default')
                user = update_form.save()
                user.password = hashed
                user.save()
                return JsonResponse({'error': False, 'msg': 'update yeee'})
            else:
                return JsonResponse({'error': True, 'msg': update_form.errors})
        else:
            return HttpResponse(update_form.as_p())


def delete_user(request, pk):
    if not request.session.exists(request.session.session_key):
        return redirect('login')
    else:
        user = User.objects.get(id=pk)
        if request.is_ajax() and request.method == 'POST':
            if user.email == request.session.get('email'):
                return JsonResponse({'error': True, 'msg': 'Can\'t delete yourself'})
            else:
                user.delete()
                return JsonResponse({'error': False, 'msg': 'update yeee'})
        else:
            form = UserForm()
            ctx = {'form': form}
            return render(request, 'main.html', ctx)
