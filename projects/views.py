# projects/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm
from .models import Project
from tasks.models import Task
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def home(request):
    owned_projects = Project.objects.filter(owner=request.user)
    assigned_tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'projects/home.html', {'owned_projects': owned_projects, 'assigned_tasks': assigned_tasks})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.members.add(request.user)
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.owner and request.user not in project.members.all():
        return redirect('home')
    tasks = Task.objects.filter(project=project)
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'project': project})


@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('home')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})


@login_required
def search(request):
    query = request.GET.get('q')
    if query:
        projects = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            owner=request.user
        )
        tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            project__owner=request.user
        )
    else:
        projects = Project.objects.none()
        tasks = Task.objects.none()
    return render(request, 'projects/search.html', {'projects': projects, 'tasks': tasks, 'query': query})


from rest_framework import generics
from .serializers import ProjectSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
