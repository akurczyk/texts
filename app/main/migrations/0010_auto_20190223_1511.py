# Generated by Django 2.1.7 on 2019-02-23 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_text_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='image_url',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='text',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
