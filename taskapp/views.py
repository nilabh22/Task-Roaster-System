from task import settings
from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import task
from taskapp.decorators import admin_only, allowed_users, unauthenticated_user
from .forms import TaskForm, CommentsForm, CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from taskapp.models import Task, Comments
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login, logout
# Create your views here.

@login_required(login_url='taskapp:login')
def index(request):
    tasklist = Task.objects.all()
    context = {'tasklist': tasklist}
    return render(request, 'taskapp/index.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username= form.cleaned_data.get('username')

            group = Group.objects.get(name='user')
            user.groups.add(group)

            messages.success(request, 'Account was Successfully created for '+ username)
            return redirect('taskapp:login')

    context ={'form':form}
    return render(request, 'taskapp/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('taskapp:login')

def userPage(request):
    context={}
    return render(request, 'taskapp/user.html', context)


@login_required(login_url='taskapp:login')
@allowed_users(allowed_roles=['admin'])
def createTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        useremail = request.POST.get('email')
        username = request.POST.get('name')
        taskTitle = request.POST.get('title')
        taskDescription = request.POST.get('description')
        
        send_mail(subject='New Task Assigned',
        message =f'NEW EMAIL FROM "COMPANY NAME".\n\nHello {username},\nA new task has been assigned to you.\n\nTASK TITLE: {taskTitle}\n\nTASK DESCRIPTION: {taskDescription}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list = [useremail],
        fail_silently=False)

        if form.is_valid():
            form.save()
            return redirect('taskapp:index')
        else:
            print('form is not valid',form)
    else:
        form = TaskForm(request.GET or None)
    return render(request, 'taskapp/create_task.html',{'form': form})


@unauthenticated_user
def loginPage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request, username =username, password =password)

        if user is not None:
            login(request, user)
            return redirect('taskapp:index')
        else:
            messages.info(request,"Username or Password is Incorrect!!")

    context ={}
    return render(request, 'taskapp/login.html', context)


@login_required(login_url='taskapp:login')
@allowed_users(allowed_roles=['admin'])
def editTask(request,pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance = task)
        datecreated = task.datecreated
        form.datecreated = datecreated

        useremail = request.POST.get('email')
        username = request.POST.get('name')
        taskTitle = request.POST.get('title')
        taskDescription = request.POST.get('description')
        
        send_mail(subject='Alloted Task Added with some Changes',
        message =f'NEW EMAIL FROM "COMPANY NAME".\n\nHello {username},\nYour Previous Task has been Edited and added with some new Content.\n\nTASK TITLE: {taskTitle}\n\nTASK DESCRIPTION: {taskDescription}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list = [useremail],
        fail_silently=False)

        if form.is_valid():
            task = form.save()
            return redirect('taskapp:index')
        else:
            print('form is not valid',form)
    else:
        form = TaskForm(instance = task)
    return render(request, 'taskapp/create_task.html',{'form': form})


@login_required(login_url='taskapp:login')
@allowed_users(allowed_roles=['admin','user'])
def viewTask(request,pk):
    task = Task.objects.get(pk=pk)
    comments = Comments.objects.filter(task_id=pk)
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save()
        else:
            print('form is not valid',form)
    else:
        form = CommentsForm(request.GET or None)
    return render(request, 'taskapp/view_task.html',{'task': task,'comments': comments,'form':form})

@login_required(login_url='taskapp:login')
@allowed_users(allowed_roles=['admin'])
def deleteTask(request, pk):
	delTask = Task.objects.get(link_id=pk)
	delTask.delete()
	return redirect('taskapp:index')