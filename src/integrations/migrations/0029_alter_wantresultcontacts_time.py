# Generated by Django 5.0.1 on 2024-06-03 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0028_alter_wantresultcontacts_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wantresultcontacts',
            name='time',
            field=models.BigIntegerField(blank=True),
        ),
    ]