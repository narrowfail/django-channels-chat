# Generated by Django 3.0.7 on 2020-07-13 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200713_1039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagemodel',
            old_name='File',
            new_name='file',
        ),
    ]
