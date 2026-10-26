from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Blog

# --- ТЕСТЫ ВТОРОГО ЗАДАНИЯ (Лайки) ---
@override_settings(TEMPLATES=[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': False,
    'OPTIONS': {'loaders': [('django.template.loaders.locmem.Loader', {'blog/detail.html': 'dummy'})]},
}])
class BlogLikesTest(TestCase):
    
    def test_new_blog_has_zero_likes(self):
        blog = Blog.objects.create(title="Тест", content="Тестовый контент")
        self.assertEqual(blog.likes, 0)

    def test_detail_view_increments_likes(self):
        blog = Blog.objects.create(title="Тест лайков", content="Контент")
        self.assertEqual(blog.likes, 0) 
        
        url = reverse('blog_detail', args=[blog.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        blog.refresh_from_db()
        self.assertEqual(blog.likes, 1)


# --- ТЕСТЫ ПЕРВОГО ЗАДАНИЯ (List Detail) ---
class BlogListDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.blog1 = Blog.objects.create(title="Первый блог", content="Контент 1")
        cls.blog2 = Blog.objects.create(title="Второй блог", content="Контент 2")

    def test_1_list_status_code_and_template(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/list.html')

    def test_2_list_contains_content(self):
        response = self.client.get(reverse('blog_list'))
        self.assertContains(response, "Первый блог")
        self.assertContains(response, "Второй блог")

    def test_3_list_contains_ids(self):
        response = self.client.get(reverse('blog_list'))
        self.assertContains(response, f'/blog/{self.blog1.id}/')
        self.assertContains(response, f'/blog/{self.blog2.id}/')

    # Декоратор ниже спасает от ошибки TemplateDoesNotExist
    @override_settings(TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': False,
        'OPTIONS': {'loaders': [('django.template.loaders.locmem.Loader', {
            'blog/detail.html': '<h1>{{ blog.title }}</h1>'
        })]},
    }])
    def test_4_detail_page_opens_by_link(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Первый блог")

    def test_5_detail_wrong_id_returns_404(self):
        response = self.client.get(reverse('blog_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)