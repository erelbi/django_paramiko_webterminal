# Generated by Django 4.0.3 on 2022-03-20 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_bashscript_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='sshconnect',
            name='vnc_installed',
            field=models.BooleanField(default=False),
        ),
    ]