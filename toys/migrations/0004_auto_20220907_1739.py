# Generated by Django 3.1.14 on 2022-09-07 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('toys', '0003_bootsignal_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='BootToken',
            fields=[
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BootTokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bootsignal',
            name='bootToken',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='BootSignals', to='toys.boottoken'),
        ),
    ]