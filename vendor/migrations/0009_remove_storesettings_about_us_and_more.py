# Generated by Django 4.2.3 on 2023-09-30 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0008_alter_vendor_date_of_birth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storesettings',
            name='about_us',
        ),
        migrations.RemoveField(
            model_name='storesettings',
            name='id',
        ),
        migrations.AddField(
            model_name='vendor',
            name='themes',
            field=models.ManyToManyField(to='vendor.theme'),
        ),
        migrations.AlterField(
            model_name='storesettings',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='storesettings',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='storesettings',
            name='social_media',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='storesettings',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='store_settings', serialize=False, to='vendor.store'),
        ),
        migrations.AlterField(
            model_name='storesettings',
            name='theme',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='theme',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]