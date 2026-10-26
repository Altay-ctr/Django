from django.test import TestCase
from django.urls import reverse
from .models import Blog  # замените на ваше приложение

class BlogListDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        cls.blog1 = Blog.objects.create(title="Первый блог", content="Контент 1")
        cls.blog2 = Blog.objects.create(title="Второй блог", content="Контент 2")

    def test_list_view_status_code_and_template(self):
        """1. Проверка статус-кода и используемого шаблона для списка"""
        response = self.client.get(reverse('blog_list'))  # укажите ваш url name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')

    def test_list_contains_content_and_id(self):
        """2. Проверка, что в списке есть контент и ID (ссылки)"""
        response = self.client.get(reverse('blog_list'))
        self.assertContains(response, "Первый блог")
        self.assertContains(response, f'/blog/{self.blog1.id}/')  # ссылка на детали

    def test_detail_view_status_code(self):
        """3. Проверка статус-кода детальной страницы"""
        response = self.client.get(reverse('blog_detail', args=[self.blog1.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_contains_content_and_title(self):
        """4. Проверка, что детальная страница отображает контент и заголовок"""
        response = self.client.get(reverse('blog_detail', args=[self.blog1.id]))
        self.assertContains(response, "Первый блог")
        self.assertContains(response, "Контент 1")

    def test_detail_wrong_id_returns_404(self):
        """5. Проверка, что несуществующий ID возвращает 404"""
        response = self.client.get(reverse('blog_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)