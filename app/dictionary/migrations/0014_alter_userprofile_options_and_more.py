# Generated by Django 4.1.2 on 2023-01-07 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0013_alter_wordcardprogress_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Профиль пользователя', 'verbose_name_plural': 'Профили пользователей'},
        ),
        migrations.RemoveField(
            model_name='wordcardprogress',
            name='count',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='default_language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dictionary.language'),
        ),
        migrations.AlterField(
            model_name='wordcardprogress',
            name='score',
            field=models.IntegerField(default=0, verbose_name='знание словарной карточки (0..10)'),
        ),
    ]