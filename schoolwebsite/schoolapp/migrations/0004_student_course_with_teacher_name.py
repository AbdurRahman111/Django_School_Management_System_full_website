# Generated by Django 3.1.4 on 2020-12-06 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0003_delete_teacher_login_infor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_course_with_Teacher_name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=200)),
                ('Teacher_ID', models.CharField(max_length=200)),
                ('Teacher_Name', models.CharField(max_length=200)),
            ],
        ),
    ]
