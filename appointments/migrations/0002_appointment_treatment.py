# Generated by Django 4.2.2 on 2023-06-16 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('treatments', '0002_rename_service_treatment'),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='treatment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='treatments.treatment'),
        ),
    ]
