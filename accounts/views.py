from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


@login_required
def home_view(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'accounts/manage_users.html', {'users': users})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)

            # فحص هل تم إدخال كلمة مرور جديدة
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)  # ← التشفير الصحيح

            user.save()
            return redirect('manage_users')
    else:
        form = RegisterForm(instance=user)

    return render(request, 'accounts/edit_user.html', {'form': form, 'user': user})
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user == user:
        # لا يسمح للمستخدم بحذف نفسه
        return redirect('/manage-users/')
    user.delete()
    return redirect('manage_users')
