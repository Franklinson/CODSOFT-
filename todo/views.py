from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from contactbook.models import Contact, PhoneNumber
from contactbook.filters import ContactFilter
from password.models import Password


def TodoList(request):
    todos = Todo.objects.all()
    total = todos.count()
    completed = Todo.objects.filter(completed=True).count()
    contacts = Contact.objects.all()
    contact = Contact.objects.get()
    phone = contact.phone_numbers.all()
    password = Password.objects.all()
    tot = contacts.count()
    myfilter = ContactFilter(request.GET, queryset=contacts)
    contacts = myfilter.qs
    
    context = {
        'todos': todos,
        'total': total,
        'completed': completed,
        'contacts': contacts,
        'tot': tot,
        'phone': phone,
        'myfilter': myfilter,
        'password': password,
    }
    return render(request, 'todo_list.html', context)

@login_required(login_url="/")
def TodoDetail(request, pk):
    todo = Todo.objects.get(id=pk)
    context = {
        'todo': todo,
    }
    return render(request, 'todo_detail.html', context)

@login_required(login_url="/")
def createTodo(request):
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    context = {
        'form': form,
    }
    return render(request, 'todo_form.html', context)

@login_required(login_url="/")
def editTodo(request, pk):
    todo = Todo.objects.get(id=pk)
    form = EditTodo(instance=todo)
    if request.method == 'POST':
        form = EditTodo(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_detail', pk=todo.pk) 
    context = {
        'form': form,
    }
    return render(request, 'edit_todo.html', context)

@login_required(login_url="/")
def deleteTodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'delete.html', {'rem': todo})



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created successfully for ' + username)
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'login.html', context)


@login_required(login_url="/")
def logoutuser(request):
    logout(request)
    return redirect('login')