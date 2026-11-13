from datetime import timedelta
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from .models import BlogPost

class BlogTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user("owner", password="StrongPass123")
        self.other = User.objects.create_user("other", password="StrongPass123")
        self.old = BlogPost.objects.create(title="Older", text="Old body", owner=self.author)
        self.new = BlogPost.objects.create(title="Newer", text="New body", owner=self.other)
        BlogPost.objects.filter(pk=self.old.pk).update(date_added=self.new.date_added - timedelta(days=1))
        self.old.refresh_from_db()

    def test_public_index_is_newest_first(self):
        response = self.client.get(reverse("blogs:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["posts"]), [self.new, self.old])

    def test_detail_is_public(self):
        self.assertContains(self.client.get(reverse("blogs:detail", args=[self.old.pk])), "Old body")

    def test_only_author_can_edit(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(reverse("blogs:edit", args=[self.old.pk])).status_code, 404)
        self.client.force_login(self.author)
        self.client.post(reverse("blogs:edit", args=[self.old.pk]), {"title": "Updated", "text": "Changed"})
        self.old.refresh_from_db()
        self.assertEqual(self.old.title, "Updated")

    def test_create_assigns_author_and_logout_is_post_only(self):
        self.client.force_login(self.author)
        self.client.post(reverse("blogs:create"), {"title": "Mine", "text": "Text"})
        self.assertTrue(BlogPost.objects.filter(title="Mine", owner=self.author).exists())
        self.assertEqual(self.client.get(reverse("users:logout")).status_code, 405)

    def test_empty_and_anonymous_create(self):
        BlogPost.objects.all().delete()
        self.assertContains(self.client.get(reverse('blogs:index')), 'Публикаций пока нет')
        self.assertEqual(self.client.get(reverse('blogs:create')).status_code, 302)

    def test_missing_and_spoofed_owner(self):
        self.client.force_login(self.author)
        self.assertEqual(self.client.get(reverse('blogs:edit', args=[999999])).status_code, 404)
        self.client.post(reverse('blogs:create'), {'title': 'Spoofed', 'text': 'Text', 'owner': self.other.pk})
        self.assertEqual(BlogPost.objects.get(title='Spoofed').owner, self.author)
        self.client.post(reverse('blogs:edit', args=[self.old.pk]), {'title': 'Edited', 'text': 'Text', 'owner': self.other.pk})
        self.old.refresh_from_db()
        self.assertEqual(self.old.owner, self.author)

    def test_invalid_form_and_public_read(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('blogs:create'), {'title': '', 'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.client.logout()
        self.assertContains(self.client.get(reverse('blogs:index')), 'Old body')

    def test_registration_and_logout(self):
        response = self.client.post(reverse('users:register'), {'username': 'newreader', 'password1': 'StrongPass123!', 'password2': 'StrongPass123!'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.get(reverse('users:logout')).status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.post(reverse('users:logout')).status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.author)
        self.assertEqual(client.post(reverse('blogs:create'), {'title': 'No token', 'text': 'Text'}).status_code, 403)
        self.assertEqual(client.post(reverse('users:logout')).status_code, 403)

    def test_required_paths(self):
        self.assertEqual(reverse('blogs:create'), '/posts/new/')
        self.assertEqual(reverse('blogs:edit', args=[7]), '/posts/7/edit/')
