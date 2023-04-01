# Generated by Django 4.1.2 on 2023-03-25 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0020_alter_cardgroup_cards_alter_wordcard_transcription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardgroup',
            name='cards',
        ),
        migrations.AddField(
            model_name='wordcard',
            name='card_groups',
            field=models.ManyToManyField(blank=True, null=True, to='dictionary.cardgroup', verbose_name='словарные группы'),
        ),
    ]
