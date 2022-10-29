# Generated by Django 4.1.2 on 2022-10-20 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dictionary", "0002_alter_language_options_alter_word_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cardgroup",
            options={"verbose_name": "подборка", "verbose_name_plural": "подборки"},
        ),
        migrations.CreateModel(
            name="WordCardProgress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "score",
                    models.IntegerField(
                        default=0, verbose_name="прогресс изучения от 0 до 1"
                    ),
                ),
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dictionary.wordcard",
                    ),
                ),
            ],
        ),
    ]