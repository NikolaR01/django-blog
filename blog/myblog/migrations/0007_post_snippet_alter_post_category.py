# Generated by Django 4.0 on 2022-01-03 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0006_alter_post_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='snippet',
            field=models.CharField(default=' New Post! ', max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(default='Life', max_length=255),
        ),
    ]