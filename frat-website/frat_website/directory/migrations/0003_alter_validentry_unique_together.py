# Generated by Django 5.0.6 on 2024-05-29 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0002_validentry'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='validentry',
            unique_together={('first_name', 'last_name', 'phone_number', 'brother_letters')},
        ),
    ]
