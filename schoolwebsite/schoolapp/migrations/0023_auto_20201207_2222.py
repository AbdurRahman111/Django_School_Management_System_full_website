# Generated by Django 3.1.4 on 2020-12-07 16:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0022_auto_20201207_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment_upload_file_image',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 7, 22, 22, 26, 452122)),
        ),
        migrations.AlterField(
            model_name='assignment_upload_file_image',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 7, 22, 22, 26, 452122)),
        ),
        migrations.CreateModel(
            name='Submit_Assignment_stu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to='uploads/stu_assignment_doc')),
                ('Student_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolapp.student_login_informatn')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolapp.student_courses_with_teacher_name')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolapp.assignment_upload_file_image')),
            ],
        ),
    ]
