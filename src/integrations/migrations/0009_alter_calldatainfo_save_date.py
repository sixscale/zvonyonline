# Generated by Django 5.0.1 on 2024-02-07 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0008_calldatainfo_delete_dialogs_delete_qualifiedleads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calldatainfo',
            name='save_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
