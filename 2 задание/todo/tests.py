from django.test import TestCase, Client
from django.urls import reverse
from .models import Task


class TaskCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_task_list_view_returns_200(self):
        response = self.client.get(reverse('todo:task_list'))
        self.assertEqual(response.status_code, 200)

    def test_task_list_shows_tasks(self):
        task = Task.objects.create(title='Тестовая задача', description='Описание')
        response = self.client.get(reverse('todo:task_list'))
        self.assertContains(response, task.title)
        self.assertContains(response, task.description)

    def test_task_create_get_returns_200(self):
        response = self.client.get(reverse('todo:task_create'))
        self.assertEqual(response.status_code, 200)

    def test_task_create_post_creates_task(self):
        data = {'title': 'Новая задача', 'description': 'Текст', 'completed': False}
        response = self.client.post(reverse('todo:task_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo:task_list'))
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.get()
        self.assertEqual(task.title, 'Новая задача')
        self.assertEqual(task.description, 'Текст')
        self.assertFalse(task.completed)

    def test_task_detail_returns_200_and_shows_task(self):
        task = Task.objects.create(title='Задача для просмотра', description='Описание')
        response = self.client.get(reverse('todo:task_detail', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.title)
        self.assertContains(response, task.description)

    def test_task_detail_404_for_invalid_pk(self):
        response = self.client.get(reverse('todo:task_detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)

    def test_task_update_get_returns_200(self):
        task = Task.objects.create(title='Исходная', description='Описание')
        response = self.client.get(reverse('todo:task_edit', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.title)

    def test_task_update_post_updates_task(self):
        task = Task.objects.create(title='Было', description='Старое')
        data = {'title': 'Стало', 'description': 'Новое', 'completed': False}
        response = self.client.post(reverse('todo:task_edit', kwargs={'pk': task.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo:task_list'))
        task.refresh_from_db()
        self.assertEqual(task.title, 'Стало')
        self.assertEqual(task.description, 'Новое')

    def test_task_delete_get_returns_200(self):
        task = Task.objects.create(title='На удаление', description='')
        response = self.client.get(reverse('todo:task_delete', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.title)

    def test_task_delete_post_deletes_task(self):
        task = Task.objects.create(title='Удаляемая', description='')
        response = self.client.post(reverse('todo:task_delete', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo:task_list'))
        self.assertEqual(Task.objects.count(), 0)
