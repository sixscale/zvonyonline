# Generated by Django 5.0.1 on 2024-01-19 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0003_rename_leads_mainleads_alter_mainleads_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=255, null=True)),
                ('site', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('project_id', models.IntegerField(blank=True, null=True)),
                ('add_date', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Leads',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='MainLeads',
        ),
    ]
