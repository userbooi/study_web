# Generated by Django 4.2.13 on 2024-07-13 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_app', '0014_alter_multiplechoicechoice_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mathmain',
            name='image',
            field=models.BinaryField(editable=True),
        ),
    ]
