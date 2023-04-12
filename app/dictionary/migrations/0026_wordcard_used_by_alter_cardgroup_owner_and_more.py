# Generated by Django 4.1.2 on 2023-04-01 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
        ('dictionary', '0025_rename_user_wordcardprogress_owner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordcard',
            name='used_by',
            field=models.ManyToManyField(related_name='shared_wordcards', to='userprofile.userprofile'),
        ),
        migrations.AlterField(
            model_name='cardgroup',
            name='owner',
            field=models.ManyToManyField(related_query_name='card_groups', to='userprofile.userprofile', verbose_name='создатель'),
        ),
        migrations.AlterField(
            model_name='wordcard',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wordcards', to='userprofile.userprofile', verbose_name='создатель'),
        ),
    ]
