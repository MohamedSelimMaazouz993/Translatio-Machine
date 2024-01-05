# Generated by Django 5.0 on 2024-01-01 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('source_language', models.CharField(max_length=10)),
                ('target_language', models.CharField(max_length=10)),
                ('translated_text', models.TextField()),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='audio/')),
            ],
        ),
    ]
