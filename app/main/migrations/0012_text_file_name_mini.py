# Generated by Django 2.2.6 on 2019-10-15 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20190223_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='file_name_mini',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]