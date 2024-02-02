from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from todo.forms import TaskCreateForm
from todo.models import Task


class TaskListView(ListView):
    model = Task
    template_name = 'todo/task_list.html'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'todo/task_detail.html'
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        return get_object_or_404(Task.objects, pk=self.kwargs[self.pk_url_kwarg])


class TaskCreateView(CreateView):
    form_class = TaskCreateForm
    template_name = 'todo/task_create.html'
    success_url = reverse_lazy('todo:task_list')

class TaskUpdateView(UpdateView):
    pass






