# Generated by Django 4.2.5 on 2023-10-05 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_pdf_file_cluster_txt_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cluster',
            name='openai_api_key',
        ),
    ]
