# Generated by Django 3.1 on 2020-09-08 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='timestamp',
            new_name='pub_date',
        ),
    ]
