# Generated by Django 4.2.3 on 2023-09-28 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_store_theme_storesettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='identity',
            field=models.FileField(null=True, upload_to='vendors/identities/'),
        ),
    ]
