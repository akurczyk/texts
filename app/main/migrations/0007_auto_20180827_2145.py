# Generated by Django 2.1 on 2018-08-27 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20180815_2337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='text',
            options={'permissions': (('edit_text', 'Can edit text'), ('publish_text', 'Can publish text'), ('unpublish_text', 'Can unpublish text'), ('remove_text', 'Can remove text'))},
        ),
    ]