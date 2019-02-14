# Generated by Django 2.1.1 on 2019-02-10 03:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='modified_by',
            field=models.ForeignKey(blank=True, help_text='Usuario última actualización', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modificado_por', to=settings.AUTH_USER_MODEL),
        ),
    ]
