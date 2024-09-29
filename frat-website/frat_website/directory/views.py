import csv
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, ForgotPasswordForm, ValidEntryImportForm, ValidEntryForm
from .models import ValidEntry

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('directory')
        else:
            error_message = 'Invalid username or password'
    return render(request, 'directory/login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def directory_view(request):
    user = request.user
    is_admin = user.is_superuser or user.groups.filter(name='Admin').exists()
    return render(request, 'directory/directory.html', {'user': user, 'is_admin': is_admin})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'directory/signup.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Notify the admin
            send_mail(
                'Forgot Password Request',
                f'The user with email {email} has requested to reset their password.',
                settings.DEFAULT_FROM_EMAIL,  # Sender email address
                [settings.ADMIN_EMAIL],       # Recipient email address (admin)
                fail_silently=False,
            )
            return render(request, 'directory/forgot_password_done.html')
    else:
        form = ForgotPasswordForm()
    return render(request, 'directory/forgot_password.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Admin').exists())
def import_valid_entries(request):
    if request.method == 'POST':
        form = ValidEntryImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            reader = csv.reader(file.read().decode('utf-8').splitlines())
            for row in reader:
                first_name, last_name, phone_number, brother_letters = row
                ValidEntry.objects.get_or_create(
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    brother_letters=brother_letters
                )
            return redirect('admin:directory_validentry_changelist')
    else:
        form = ValidEntryImportForm()
    return render(request, 'directory/import_valid_entries.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Admin').exists())
def add_valid_entry(request):
    if request.method == 'POST':
        form = ValidEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:directory_validentry_changelist')
    else:
        form = ValidEntryForm()
    return render(request, 'directory/add_valid_entry.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Admin').exists())
def executive_board_view(request):
    return render(request, 'directory/executive_board.html')

def index_view(request):
    return redirect('login')
