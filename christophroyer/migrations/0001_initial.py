# Generated by Django 2.2.13 on 2020-07-30 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_en', models.CharField(max_length=255)),
                ('name_de', models.CharField(max_length=255)),
                ('text_en', models.TextField()),
                ('text_de', models.TextField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-time_created',),
            },
        ),
    ]
