# Generated by Django 5.0.7 on 2024-07-31 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_site', '0003_menulink_site_setup'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetup',
            name='favicon',
            field=models.ImageField(blank=True, default='', upload_to='assets/favicon/%Y/%m'),
        ),
    ]
