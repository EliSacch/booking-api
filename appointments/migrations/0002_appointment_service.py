# Generated by Django 4.2.1 on 2023-06-11 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('allservices', '0001_initial'),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='allservices.service'),
        ),
    ]