# Generated by Django 4.2.13 on 2024-07-20 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_app', '0017_chemsubunit_image_compscisubunit_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='solution',
            field=models.BinaryField(default=b'\x00\x00', editable=True),
        ),
    ]
