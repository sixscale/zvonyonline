# Generated by Django 5.0.1 on 2024-02-16 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0019_alter_calldatainfo_call_call_project_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calldatainfo',
            name='call_result_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]