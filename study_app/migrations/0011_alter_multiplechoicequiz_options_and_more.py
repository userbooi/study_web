# Generated by Django 5.0.4 on 2024-07-03 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_app', '0010_multiplechoicequiz_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='multiplechoicequiz',
            options={'verbose_name_plural': 'multiple choice quizzes'},
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='quiz',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='study_app.multiplechoicequiz'),
            preserve_default=False,
        ),
    ]
