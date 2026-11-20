from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['name', 'surname'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
