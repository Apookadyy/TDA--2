from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post      # change this import according to your app models

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

    def test_user_login(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpassword123"
        })
        self.assertEqual(response.status_code, 302)  # redirect after login

    def test_user_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "MyNewPassword@123",
            "password2": "MyNewPassword@123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="postuser",
            password="pass12345"
        )
        self.post = Post.objects.create(
            user=self.user,
            content="This is a test post"
        )

    def test_post_created(self):
        self.assertEqual(self.post.content, "This is a test post")
        self.assertEqual(self.post.user.username, "postuser")
        self.assertTrue(Post.objects.count(), 1)


class PostViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="demo",
            password="password123"
        )
        self.client.login(username="demo", password="password123")
        Post.objects.create(user=self.user, content="Hello world!")

    def test_post_list_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello world!")

    def test_create_post(self):
        response = self.client.post(reverse("create_post"), {
            "content": "New post created!"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content="New post created!").exists())


class URLTests(TestCase):
    def test_home_url(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, [200, 302])

    def test_login_url(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

