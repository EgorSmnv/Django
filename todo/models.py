from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Task(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=255, blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_finish = models.DateTimeField(verbose_name="Время окончания")
    is_finished = models.BooleanField(blank=False, default=False, verbose_name="Завершена")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='tasks', null=True, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todo:task_detail', kwargs={'task_id': self.pk})
