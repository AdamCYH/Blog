# Generated by Django 3.1.7 on 2021-03-15 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210314_2336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='name',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='image',
            name='url',
        ),
    ]
