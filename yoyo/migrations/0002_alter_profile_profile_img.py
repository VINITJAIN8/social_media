# Generated by Django 4.2.5 on 2023-09-24 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yoyo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
