# Generated by Django 5.1.6 on 2025-02-18 16:03

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isbn', models.CharField(max_length=17, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('available', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
