# Generated by Django 4.2.1 on 2023-06-01 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField()),
                ('time', models.IntegerField(choices=[(900, '9:00'), (950, '9:30'), (1000, '10:00'), (1050, '10:30'), (1100, '11:00'), (1150, '11:30'), (1200, '12:00'), (1250, '12:30'), (1300, '13:00'), (1350, '13:30'), (1400, '14:00'), (1450, '14:30'), (1500, '15:00'), (1550, '15:30'), (1600, '16:00'), (1650, '16:30')], default=900)),
                ('end_time', models.IntegerField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='services.service')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
