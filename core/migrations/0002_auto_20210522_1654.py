# Generated by Django 3.0.14 on 2021-05-22 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roommodel',
            old_name='title',
            new_name='name',
        ),
    ]