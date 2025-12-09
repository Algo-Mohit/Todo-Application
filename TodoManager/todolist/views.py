from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Task
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    success = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject="New Contact Form Message",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        success = True

    return render(request, "contact.html", {"success": success})
def home(request):
    context = {
        'page':'home'
    }
    return render(request,"home.html",context)


def about(request):
    return render(request, "about.html")


@login_required
def task_delete(request,task_id):
    task1 = Task.objects.get(id = task_id)
    if task1.owner == request.user:
        task1.delete()
        messages.success(request,f"Task : {task1.task_name} delete successfully")
        return redirect("todolist")
    else:
        messages.error(request,"You are not allow to delete task!!")

@login_required
def task_edit(request,task_id):
    task1 = Task.objects.get(id = task_id)
    if request.method == "POST":
        form_data = TaskForm(request.POST or None , instance=task1)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,"Task updated!!")
            return redirect("todolist") 
        messages.success(request,"Error in updation") 
    else:
        context = {
            'task1':task1
        }
        return render(request,"edit.html",context)

@login_required    
def update_status(request,task_id):
    task1 = Task.objects.get(id = task_id)
    if task1.owner == request.user:
        if task1.is_completed == False:
            task1.is_completed = True
            task1.save()     
        else:
            task1.is_completed = False
            task1.save()   
        messages.success(request,"Status updated!!")
        return redirect("todolist")   
    else:
        messages.error(request,"You are not allow to change the status!!")




@login_required
def todolist(request):
    if request.method == 'POST':
        form_data = TaskForm(request.POST or None)
        if form_data.is_valid():
            instance = form_data.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request,"Task added successfully")
            return redirect("todolist")  

    task = Task.objects.filter(owner = request.user)
    #for pagination
    paginator = Paginator(task,5)
    page = request.GET.get("page")
    #reload 
    task = paginator.get_page(page)
    context = {
        'all_task':task
    }
    return render(request,"todolist.html",context)

