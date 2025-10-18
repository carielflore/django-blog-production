from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from blog.models import Post, Category, Location, Comment
from blog.forms import PostForm, CommentForm

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            title='Test Category',
            description='Test Description',
            slug='test-category'
        )
        self.location = Location.objects.create(
            name='Test Location'
        )
        # Добавим общую дату для всех тестов
        self.test_date = timezone.now()

    def test_post_creation(self):
        """Тест создания поста"""
        post = Post.objects.create(
            title='Test Post',
            text='Test content',
            pub_date=self.test_date,  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
            author=self.user,
            category=self.category,
            location=self.location
        )
        self.assertEqual(str(post), 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertTrue(post.is_published)

    def test_comment_creation(self):
        """Тест создания комментария"""
        post = Post.objects.create(
            title='Test Post',
            text='Test content',
            pub_date=self.test_date,  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
            author=self.user,
            category=self.category
        )
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            text='Test comment'
        )
        self.assertEqual(str(comment), 'Test comment')
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.author, self.user)

    def test_post_comment_count(self):
        """Тест свойства comment_count"""
        post = Post.objects.create(
            title='Test Post',
            text='Test content',
            pub_date=self.test_date,  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
            author=self.user,
            category=self.category
        )
        Comment.objects.create(
            post=post,
            author=self.user,
            text='First comment'
        )
        Comment.objects.create(
            post=post,
            author=self.user,
            text='Second comment'
        )
        self.assertEqual(post.comment_count, 2)


class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            title='Test Category',
            description='Test Description',
            slug='test-category'
        )
        self.location = Location.objects.create(
            name='Test Location'
        )
        self.test_date = timezone.now()  # ← ДОБАВЬТЕ

    def test_post_form_valid(self):
        """Тест валидной формы поста"""
        form_data = {
            'title': 'Test Post',
            'text': 'Test content',
            'pub_date': self.test_date.strftime('%Y-%m-%dT%H:%M'),  # ← ИСПРАВЬТЕ ФОРМАТ
            'category': self.category.id,
            'location': self.location.id,
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_save_with_author(self):
        """Тест сохранения формы поста с автором"""
        form_data = {
            'title': 'Test Post',
            'text': 'Test content',
            'pub_date': self.test_date.strftime('%Y-%m-%dT%H:%M'),  # ← ИСПРАВЬТЕ ФОРМАТ
            'category': self.category.id,
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        post = form.save(commit=False, author=self.user)
        post.save()
        
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, 'Test Post')

    def test_comment_form_valid(self):
        """Тест валидной формы комментария"""
        form_data = {
            'text': 'Test comment text'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            title='Test Category',
            description='Test Description',
            slug='test-category',
            is_published=True
        )
        self.post = Post.objects.create(
            title='Test Post',
            text='Test content',
            pub_date=timezone.now() - timezone.timedelta(days=1),
            author=self.user,
            category=self.category,
            is_published=True
        )

    def test_home_page_status_code(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page(self):
        """Тест страницы деталей поста"""
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_category_page(self):
        """Тест страницы категории"""
        response = self.client.get(
            reverse('blog:category_posts', kwargs={'category_slug': self.category.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.title)

    def test_profile_page(self):
        """Тест страницы профиля"""
        response = self.client.get(
            reverse('blog:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.status_code, 200)

    def test_login_required_views(self):
        """Тест что защищенные views требуют авторизации"""
        protected_urls = [
            reverse('blog:create_post'),
            reverse('blog:edit_post', kwargs={'post_id': self.post.id}),
            reverse('blog:delete_post', kwargs={'post_id': self.post.id}),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [302, 403, 404])


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            title='Test Category',
            description='Test Description',
            slug='test-category',
            is_published=True
        )
        self.test_date = timezone.now()

    def test_login_required_functionality(self):
        """Тест функционала требующего авторизации после логина"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('blog:create_post'))
        self.assertIn(response.status_code, [200, 405])


class BusinessLogicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            title='Test Category',
            description='Test Description',
            slug='test-category',
            is_published=True
        )
        self.test_date = timezone.now()

    def test_unpublished_post_not_visible(self):
        """Тест что неопубликованный пост не виден"""
        post = Post.objects.create(
            title='Unpublished Post',
            text='Test content',
            pub_date=self.test_date - timezone.timedelta(days=1),
            author=self.user,
            category=self.category,
            is_published=False
        )
        
        response = self.client.get(reverse('blog:index'))
        self.assertNotContains(response, 'Unpublished Post')

    def test_future_post_not_visible(self):
        """Тест что пост с будущей датой не виден"""
        post = Post.objects.create(
            title='Future Post',
            text='Test content',
            pub_date=self.test_date + timezone.timedelta(days=1),
            author=self.user,
            category=self.category,
            is_published=True
        )
        
        response = self.client.get(reverse('blog:index'))
        self.assertNotContains(response, 'Future Post')


class IntegrationTests(TestCase):
    """Интеграционные тесты полного flow"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            title='Test Category',
            description='Test Description',
            slug='test-category',
            is_published=True
        )
        self.test_date = timezone.now()

    def test_full_post_creation_flow(self):
        """Полный тест flow создания поста и комментария"""
        # Логин
        self.client.login(username='testuser', password='testpass123')
        
        # Создание поста
        post_data = {
            'title': 'Integration Test Post',
            'text': 'Integration test content',
            'pub_date': self.test_date.strftime('%Y-%m-%dT%H:%M'),
            'category': self.category.id,
        }
        
        response = self.client.post(
            reverse('blog:create_post'),
            post_data
        )
        self.assertEqual(response.status_code, 302)
        
        # Получаем созданный пост
        post = Post.objects.get(title='Integration Test Post')
        
        # Создание комментария
        comment_data = {
            'text': 'Integration test comment'
        }
        
        response = self.client.post(
            reverse('blog:add_comment', kwargs={'post_id': post.id}),
            comment_data
        )
        self.assertEqual(response.status_code, 302)
        
        # Проверяем что комментарий создан
        self.assertEqual(post.comments.count(), 1)
        self.assertEqual(post.comments.first().text, 'Integration test comment')
