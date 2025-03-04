# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
from projects.models import Project
from django.contrib.auth.decorators import login_required

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.owner and request.user not in project.members.all():
        return redirect('home')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()
        form.fields['assigned_to'].queryset = project.members.all()
    return render(request, 'tasks/task_form.html', {'form': form, 'project': project})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user != task.project.owner:
        return redirect('home')
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)
        form.fields['assigned_to'].queryset = task.project.members.all()
    return render(request, 'tasks/task_form.html', {'form': form, 'project': task.project})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user != task.project.owner:
        return redirect('home')
    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', project_id=task.project.id)
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user == task.assigned_to or request.user == task.project.owner:
        task.completed = not task.completed
        task.save()
    return redirect('project_detail', project_id=task.project.id)