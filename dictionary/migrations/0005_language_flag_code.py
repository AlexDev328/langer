# Generated by Django 4.1.2 on 2022-10-20 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dictionary", "0004_alter_wordcardprogress_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="language",
            name="flag_code",
            field=models.CharField(max_length=2, null=True, verbose_name="Код"),
        ),
    ]
