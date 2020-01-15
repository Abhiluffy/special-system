# Generated by Django 2.2 on 2019-09-16 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('whitebricks', '0007_auto_20190912_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='pg',
            name='publisher',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='pg', to=settings.AUTH_USER_MODEL),
        ),
    ]