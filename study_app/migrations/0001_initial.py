# Generated by Django 5.0.4 on 2024-06-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
            ],
            options={
                'verbose_name': 'feedback',
                'verbose_name_plural': 'feedbacks',
            },
        ),
    ]
