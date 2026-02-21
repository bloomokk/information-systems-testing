from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from .models import Task
from .forms import TaskForm


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'todo/task_list.html'
    paginate_by = 10


class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task_detail.html'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('todo:task_list')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    context_object_name = 'task'
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('todo:task_list')


class TaskDeleteView(DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task_confirm_delete.html'
    success_url = reverse_lazy('todo:task_list')


def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    next_url = request.GET.get('next') or reverse('todo:task_list')
    return redirect(next_url)
