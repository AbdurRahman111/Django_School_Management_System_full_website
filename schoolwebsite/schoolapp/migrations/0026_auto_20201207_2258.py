# Generated by Django 3.1.4 on 2020-12-07 16:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0025_auto_20201207_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment_upload_file_image',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 7, 22, 58, 52, 262109)),
        ),
        migrations.AlterField(
            model_name='assignment_upload_file_image',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 7, 22, 58, 52, 262109)),
        ),
        migrations.AlterField(
            model_name='teacher_assignment_upload_file_image',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 7, 22, 58, 52, 263108)),
        ),
        migrations.AlterField(
            model_name='teacher_assignment_upload_file_image',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 7, 22, 58, 52, 263108)),
        ),
        migrations.CreateModel(
            name='Student_Submit_Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to='uploads/stu_assignment_doc')),
                ('Assignment_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolapp.teacher_assignment_upload_file_image')),
                ('Student_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolapp.student_login_informatn')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolapp.student_courses_with_teacher_name')),
            ],
        ),
    ]