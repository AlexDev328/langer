# Generated by Django 4.1.2 on 2023-03-25 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0018_alter_cardgroup_owner_alter_wordcard_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordcard',
            name='transcription',
            field=models.CharField(max_length=255, verbose_name='транскрипция'),
        ),
    ]