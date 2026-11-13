from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('posts', '0001_initial')]
    operations = [
        migrations.RenameModel('Post', 'BlogPost'),
        migrations.RenameField('blogpost', 'body', 'text'),
        migrations.RenameField('blogpost', 'author', 'owner'),
        migrations.RenameField('blogpost', 'created_at', 'date_added'),
        migrations.AlterModelOptions('blogpost', options={'ordering': ['-date_added']}),
    ]
