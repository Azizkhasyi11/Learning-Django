from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    
    # Check is logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticated
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            messages.success(request, 'There was an error logging in. Please try again...')
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out...')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticated login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have been registered and logged in!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def costumer_record(request, pk):
    if request.user.is_authenticated:
        # Look up record
        costumer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'costumer_record': costumer_record})
    else:
        messages.success(request, 'You must be logged in to view that page...')
        return redirect('home')
    
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            delete_it = Record.objects.get(id=pk)
            delete_it.delete()
            messages.success(request, 'Record has been deleted...')
            return redirect('home')
    else:
        messages.success(request, 'You Must Log In to Delete a Record...')
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                if form.is_valid():
                    add_record = form.save()
                    messages.success(request, 'Record has been added...')
                    return redirect('home')
            return render(request, 'add_record.html', {'form': form})
        else:
            messages.success(request, 'You Must Be an Admin to Add a Record...')
            return redirect('home')
    return redirect('home')