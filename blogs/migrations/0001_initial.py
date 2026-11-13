import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="Post", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=200, verbose_name="Заголовок")), ("body", models.TextField(verbose_name="Текст")), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="blog_posts", to=settings.AUTH_USER_MODEL))], options={"ordering": ["-created_at"]})]
