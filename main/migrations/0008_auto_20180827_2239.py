# Generated by Django 2.1 on 2018-08-27 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20180827_2145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='text',
            options={'permissions': (('my_edit_text', 'CUSTOM Can edit text'), ('my_publish_text', 'CUSTOM Can publish text'), ('my_unpublish_text', 'CUSTOM Can unpublish text'), ('my_remove_text', 'CUSTOM Can remove text'))},
        ),
    ]
