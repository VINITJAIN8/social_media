# Generated by Django 4.2.5 on 2023-09-24 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yoyo', '0005_remove_profile_id_user_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
