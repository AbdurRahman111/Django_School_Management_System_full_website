# Generated by Django 3.1.4 on 2020-12-07 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0021_auto_20201207_2057'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Submit_Assignment',
        ),
        migrations.AlterField(
            model_name='assignment_upload_file_image',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 7, 20, 58, 52, 675283)),
        ),
        migrations.AlterField(
            model_name='assignment_upload_file_image',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 7, 20, 58, 52, 675283)),
        ),
    ]
