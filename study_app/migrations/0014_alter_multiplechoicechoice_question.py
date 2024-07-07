# Generated by Django 5.0.4 on 2024-07-04 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_app', '0013_alter_multiplechoicequestion_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiplechoicechoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='study_app.multiplechoicequestion'),
        ),
    ]