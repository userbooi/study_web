# Generated by Django 4.2.13 on 2024-07-13 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_app', '0015_alter_mathmain_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chemmain',
            name='image',
            field=models.BinaryField(editable=True),
        ),
        migrations.AlterField(
            model_name='compscimain',
            name='image',
            field=models.BinaryField(editable=True),
        ),
        migrations.AlterField(
            model_name='physicsmain',
            name='image',
            field=models.BinaryField(editable=True),
        ),
    ]