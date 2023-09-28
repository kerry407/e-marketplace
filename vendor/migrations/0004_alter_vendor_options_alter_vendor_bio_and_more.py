# Generated by Django 4.2.3 on 2023-09-28 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_alter_vendor_profile_img_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ['last_updated']},
        ),
        migrations.AlterField(
            model_name='vendor',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='identity',
            field=models.FileField(null=True, upload_to='vendors/identities/'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='profile_img_url',
            field=models.ImageField(null=True, upload_to='vendors/profile_images/'),
        ),
    ]
