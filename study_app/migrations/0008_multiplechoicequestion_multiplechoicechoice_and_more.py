# Generated by Django 5.0.4 on 2024-07-03 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_app', '0007_alter_chemsubunit_id_alter_chemunit_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('unit', models.CharField(max_length=250)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=150)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_app.multiplechoicequestion')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.BooleanField(default=False)),
                ('answer', models.CharField(max_length=150)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_app.multiplechoicequestion')),
            ],
        ),
    ]