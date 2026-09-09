from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user("author", password="StrongPass123")
        self.other = User.objects.create_user("other", password="StrongPass123")
        self.old = Post.objects.create(title="Older", body="Old body", author=self.author)
        self.new = Post.objects.create(title="Newer", body="New body", author=self.other)
        Post.objects.filter(pk=self.old.pk).update(created_at=self.new.created_at - timedelta(days=1))
        self.old.refresh_from_db()

    def test_public_index_is_newest_first(self):
        response = self.client.get(reverse("posts:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["posts"]), [self.new, self.old])

    def test_detail_is_public(self):
        self.assertContains(self.client.get(reverse("posts:detail", args=[self.old.pk])), "Old body")

    def test_only_author_can_edit(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(reverse("posts:edit", args=[self.old.pk])).status_code, 404)
        self.client.force_login(self.author)
        self.client.post(reverse("posts:edit", args=[self.old.pk]), {"title": "Updated", "body": "Changed"})
        self.old.refresh_from_db()
        self.assertEqual(self.old.title, "Updated")

    def test_create_assigns_author_and_logout_is_post_only(self):
        self.client.force_login(self.author)
        self.client.post(reverse("posts:create"), {"title": "Mine", "body": "Text"})
        self.assertTrue(Post.objects.filter(title="Mine", author=self.author).exists())
        self.assertEqual(self.client.get(reverse("users:logout")).status_code, 405)
