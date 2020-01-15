# Generated by Django 2.2 on 2019-09-12 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whitebricks', '0006_remove_pg_userinfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Userinfo',
        ),
        migrations.AddField(
            model_name='pg',
            name='address',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='pg',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
        migrations.AddField(
            model_name='pg',
            name='first_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='pg',
            name='last_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='pg',
            name='phone',
            field=models.IntegerField(default=None),
        ),
    ]
